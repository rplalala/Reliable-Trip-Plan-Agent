"""Bounded optional rewrite with independent meaning-preservation review."""

import asyncio
import json
import re
from collections import Counter
from collections.abc import Callable
from datetime import UTC, datetime
from threading import Lock

from pydantic import ValidationError

from backend.app.runtime.config_models import PreferencePolishingConfig
from backend.app.runtime.token_counting import count_tokens
from backend.app.schemas.input_assistance import (
    PolishDraft,
    PolishRequest,
    PolishResponse,
    PolishReview,
)
from backend.app.services.preference_polishing_prompts import (
    DRAFT_SYSTEM_PROMPT,
    REVIEW_SYSTEM_PROMPT,
)


class PolishingInputLimit(RuntimeError):
    """The optional assistance envelope is smaller than normal planning input."""


class PolishingRateLimited(RuntimeError):
    """An optional model operation is already running or the daily allowance is spent."""


class PolishingDeadline(RuntimeError):
    """The optional two-call operation exceeded its bounded deadline."""


class PolishingUnavailable(RuntimeError):
    """A model or configuration problem prevented a safe suggestion."""


class PolishingInvalidResponse(RuntimeError):
    """The model produced output that violates the assistance contract."""


_ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_NUMBER = re.compile(r"\b\d+(?:\.\d+)?\b")
_THREE_LETTER_WORD = re.compile(r"\b[A-Za-z]{3}\b")
_CURRENCY_AFTER_AMOUNT = re.compile(r"\b\d+(?:\.\d+)?\s+([A-Za-z]{3})\b")
_CURRENCY_BEFORE_AMOUNT = re.compile(r"\b([A-Za-z]{3})\s+\d+(?:\.\d+)?\b")
_KNOWN_CURRENCIES = frozenset({
    "AUD", "USD", "EUR", "GBP", "CNY", "JPY", "CAD", "NZD", "SGD", "HKD",
    "CHF", "KRW", "INR", "THB", "MYR", "IDR", "VND", "PHP", "AED", "ZAR",
})


def _explicit_tokens(text: str) -> Counter[str]:
    dates = [f"date:{match.group()}" for match in _ISO_DATE.finditer(text)]
    without_dates = _ISO_DATE.sub(" ", text)
    numbers = [f"number:{match.group()}" for match in _NUMBER.finditer(without_dates)]
    currencies = [
        f"currency:{word.upper()}"
        for word in _THREE_LETTER_WORD.findall(without_dates)
        if word.isupper() or word.upper() in _KNOWN_CURRENCIES
    ]
    currencies.extend(
        f"adjacent_currency:{match.group(1).upper()}"
        for pattern in (_CURRENCY_AFTER_AMOUNT, _CURRENCY_BEFORE_AMOUNT)
        for match in pattern.finditer(without_dates)
    )
    return Counter([*dates, *numbers, *currencies])


def _prompt_payload(request: PolishRequest, candidate: str | None = None) -> str:
    data = {
        "original_text": request.original_text,
        "read_only_context": request.context.model_dump(mode="json", exclude_none=True),
    }
    if candidate is not None:
        data["candidate_text"] = candidate
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


class PreferencePolishingService:
    def __init__(
        self,
        client_factory: Callable,
        config: PreferencePolishingConfig | None = None,
        *,
        utc_now=lambda: datetime.now(UTC),
    ) -> None:
        self._client_factory = client_factory
        self._config = config or PreferencePolishingConfig()
        self._utc_now = utc_now
        self._lock = Lock()
        self._day = None
        self._count = 0
        self._inflight = False

    def _admit(self) -> None:
        with self._lock:
            day = self._utc_now().date()
            if day != self._day:
                self._day, self._count = day, 0
            if self._inflight or self._count >= self._config.daily_operations_per_process:
                raise PolishingRateLimited()
            self._inflight = True
            self._count += 1

    def _release(self) -> None:
        with self._lock:
            self._inflight = False

    def _fits_model_input(self, system: str, user: str, schema) -> bool:
        total = count_tokens(system) + count_tokens(user)
        total += count_tokens(json.dumps(schema.model_json_schema(), sort_keys=True))
        return total <= self._config.model_input_tokens_per_call

    async def polish(self, request: PolishRequest) -> PolishResponse:
        original = request.original_text
        if (
            len(original) > self._config.source_max_chars
            or count_tokens(original) > self._config.source_max_tokens
        ):
            raise PolishingInputLimit()
        draft_user = _prompt_payload(request)
        if not self._fits_model_input(DRAFT_SYSTEM_PROMPT, draft_user, PolishDraft):
            raise PolishingInputLimit()
        self._admit()
        client = None
        try:
            try:
                client = self._client_factory()
            except Exception as exc:
                raise PolishingUnavailable() from exc
            try:
                async with asyncio.timeout(self._config.total_timeout_seconds):
                    draft = await asyncio.wait_for(
                        client.draft(
                            DRAFT_SYSTEM_PROMPT, draft_user, self._config.draft_output_tokens
                        ),
                        timeout=self._config.call_timeout_seconds,
                    )
                    draft = PolishDraft.model_validate(draft)
                    if draft.status != "suggested":
                        return PolishResponse(
                            status=draft.status,
                            original_text=original,
                            suggested_text=None,
                            explanation=draft.explanation,
                            questions=draft.questions,
                            client_revision=request.client_revision,
                        )
                    candidate = draft.suggested_text or ""
                    review_user = _prompt_payload(request, candidate)
                    if not self._fits_model_input(REVIEW_SYSTEM_PROMPT, review_user, PolishReview):
                        return self._needs_input(
                            request, "The proposed wording is too long to verify."
                        )
                    review = await asyncio.wait_for(
                        client.review(
                            REVIEW_SYSTEM_PROMPT, review_user, self._config.review_output_tokens
                        ),
                        timeout=self._config.call_timeout_seconds,
                    )
                    review = PolishReview.model_validate(review)
                    if review.verdict != "preserved" or _explicit_tokens(
                        original
                    ) != _explicit_tokens(candidate):
                        return self._needs_input(
                            request, "The proposed wording may change your meaning."
                        )
                    return PolishResponse(
                        status="suggested",
                        original_text=original,
                        suggested_text=candidate,
                        explanation=draft.explanation,
                        questions=[],
                        client_revision=request.client_revision,
                    )
            except TimeoutError as exc:
                raise PolishingDeadline() from exc
            except ValidationError as exc:
                raise PolishingInvalidResponse() from exc
            except ValueError as exc:
                raise PolishingUnavailable() from exc
        finally:
            try:
                if client is not None and hasattr(client, "aclose"):
                    try:
                        await client.aclose()
                    except Exception:
                        pass
            finally:
                self._release()

    @staticmethod
    def _needs_input(request: PolishRequest, explanation: str) -> PolishResponse:
        return PolishResponse(
            status="needs_input",
            original_text=request.original_text,
            suggested_text=None,
            explanation=explanation,
            questions=["Please review the original wording before trying again."],
            client_revision=request.client_revision,
        )
