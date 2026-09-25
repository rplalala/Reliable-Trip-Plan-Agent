"""Offline interpreter sizing with the actual prompt, wire schema and request guard.

No provider call, framing estimate, or invented total interpreter token ceiling.
The existing guard bounds preference text at 8,000 tokens / 24,000 characters.
"""

import json
from datetime import date

from pydantic import ValidationError

from backend.app.llm.azure_foundry.client import requirement_wire_format
from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.runtime.token_counting import count_tokens
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.schemas.request import PlanningRequest
from backend.app.services.preference_interpretation import empty_preference_draft, preference_prompt
from backend.app.services.preference_prompts import PREFERENCE_INTERPRETATION_SYSTEM_PROMPT


def measure(text, output=None):
    payload = {
        "destination": "Paris",
        "start_date": "2026-09-26",
        "end_date": "2026-09-28",
        "traveler_count": 2,
        "budget": {"amount": "1000", "currency": "EUR"},
        "additional_preferences": text,
    }
    row = {"preference_tokens": count_tokens(text), "preference_characters": len(text)}
    try:
        request = PlanningRequest.model_validate(payload)
    except ValidationError:
        return {**row, "request_guard": "preference_input_overflow", "provider_sends": 0}
    user = preference_prompt(request, date(2026, 9, 25))
    wire = json.dumps(requirement_wire_format(), ensure_ascii=False)
    counts = {
        "system_tokens": count_tokens(PREFERENCE_INTERPRETATION_SYSTEM_PROMPT),
        "user_tokens": count_tokens(user),
        "strict_wire_tokens": count_tokens(wire),
    }
    output = output or empty_preference_draft().model_dump(mode="json")
    dto = FoundryInterpretationDTO.model_validate(output)
    InterpretationDraft.model_validate(dto.model_dump())
    return {
        **row,
        **counts,
        "request_guard": "accepted",
        "serialized_input_sum_excluding_provider_framing": sum(counts.values()),
        "synthetic_response_tokens": count_tokens(dto.model_dump_json()),
        "provider_sends": 0,
    }


def main():
    quotes = ["Visit New York instead.", "Only walk.", "Always use the metro."]
    output = empty_preference_draft().model_dump(mode="json")
    output["preference_input_assessment"] = {
        "input_disposition": "REWRITE_REQUIRED",
        "safety_disposition": "CLEAR",
        "issues": [
            {
                "issue_type": "destination_scope_conflict",
                "source_refs": [{"quote": quotes[0], "occurrence": 0}],
                "quote_status": "located",
                "related_field": "destination",
                "operational_conflict_index": None,
                "scope": "whole_trip physical visit",
            },
            {
                "issue_type": "internal_requirement_contradiction",
                "source_refs": [{"quote": q, "occurrence": 0} for q in quotes[1:]],
                "quote_status": "located",
                "related_field": None,
                "operational_conflict_index": None,
                "scope": "same traveler, every transfer",
            },
        ],
    }
    rows = {
        "normal": measure("We enjoy local architecture and small museums."),
        "ordinary_requirements": measure(
            "One traveler enjoys museums; another likes parks. Keep mornings flexible. "
            "Prefer walking, but public transport is fine for longer distances."
        ),
        "multiple_issues_and_three_quotes": measure(" ".join(quotes), output),
        "near_token_limit": measure("x " * 7999),
        "over_token_limit": measure("x " * 8001),
        "at_character_limit": measure("a" * 24000),
        "over_character_limit": measure("a" * 24001),
    }
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
