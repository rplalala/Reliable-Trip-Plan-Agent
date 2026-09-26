"""Dedicated two-schema Microsoft Foundry port for optional preference polishing."""

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import BadRequestError, RateLimitError
from pydantic import BaseModel, ConfigDict, ValidationError

from backend.app.schemas.input_assistance import PolishDraft, PolishReview
from backend.app.versions.v0.config import V0Settings


class PolishProviderBlocked(RuntimeError):
    """The model provider rejected the content or structured request."""


class PolishProviderThrottled(RuntimeError):
    """The model provider limited this optional operation."""


class PolishProviderUnavailable(RuntimeError):
    """The model provider could not complete a valid structured call."""


class PolishProviderInvalidResponse(RuntimeError):
    """The provider result could not be parsed or verified against the response contract."""


class _DraftWire(BaseModel):
    """Required-only schema accepted by the strict Foundry transport."""

    model_config = ConfigDict(extra="forbid")

    status: str
    suggested_text: str | None
    explanation: str
    questions: list[str]


class _ReviewWire(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: str
    reason: str


class FoundryPolishingClient:
    def __init__(self, settings: V0Settings) -> None:
        self._chat = ChatOpenAI(
            model=settings.azure_openai_deployment,
            base_url=str(settings.azure_openai_endpoint),
            api_key=settings.azure_openai_api_key.get_secret_value(),
            use_responses_api=True,
            max_retries=0,
        )

    async def aclose(self) -> None:
        try:
            await self._chat.root_async_client.close()
        finally:
            self._chat.root_client.close()

    async def _call(self, wire_schema, domain_schema, system_prompt, user_prompt, output_tokens):
        try:
            model = self._chat.with_structured_output(
                wire_schema, method="json_schema", strict=True, max_output_tokens=output_tokens
            )
            result = await model.ainvoke(
                [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            )
            if not isinstance(result, wire_schema):
                raise PolishProviderInvalidResponse()
            return domain_schema.model_validate(result.model_dump())
        except BadRequestError as exc:
            raise PolishProviderBlocked() from exc
        except RateLimitError as exc:
            raise PolishProviderThrottled() from exc
        except (ValidationError, OutputParserException) as exc:
            raise PolishProviderInvalidResponse() from exc
        except PolishProviderInvalidResponse:
            raise
        except Exception as exc:
            raise PolishProviderUnavailable() from exc

    async def draft(self, system_prompt, user_prompt, output_tokens) -> PolishDraft:
        return await self._call(_DraftWire, PolishDraft, system_prompt, user_prompt, output_tokens)

    async def review(self, system_prompt, user_prompt, output_tokens) -> PolishReview:
        return await self._call(
            _ReviewWire, PolishReview, system_prompt, user_prompt, output_tokens
        )


def create_foundry_polisher() -> FoundryPolishingClient:
    return FoundryPolishingClient(V0Settings())
