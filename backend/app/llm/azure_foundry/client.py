"""Microsoft Foundry implementation of the structured LLM client interface."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError

from backend.app.llm.azure_foundry.dto import (
    FoundryItineraryDTO,
    FoundryTravelRequirementsDTO,
)
from backend.app.llm.azure_foundry.mapping import (
    FoundryMappingError,
    map_foundry_itinerary,
    map_foundry_requirements,
)
from backend.app.llm.client import StructuredModelT, StructuredOutputError
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequirements


@dataclass(frozen=True)
class _FoundryBinding:
    transport_schema: type[BaseModel]
    to_domain: Callable[[BaseModel], BaseModel]


def _map_requirements(value: BaseModel) -> TravelRequirements:
    dto = FoundryTravelRequirementsDTO.model_validate(value)
    return map_foundry_requirements(dto)


def _map_itinerary(value: BaseModel) -> Itinerary:
    dto = FoundryItineraryDTO.model_validate(value)
    return map_foundry_itinerary(dto)


_FOUNDRY_BINDINGS: dict[type[BaseModel], _FoundryBinding] = {
    TravelRequirements: _FoundryBinding(
        transport_schema=FoundryTravelRequirementsDTO,
        to_domain=_map_requirements,
    ),
    Itinerary: _FoundryBinding(
        transport_schema=FoundryItineraryDTO,
        to_domain=_map_itinerary,
    ),
}


class AzureFoundryStructuredLLMClient:
    """Use strict transport DTOs through a Microsoft Foundry v1 endpoint."""

    def __init__(self, *, endpoint: str, deployment: str, api_key: str) -> None:
        self._chat_model = ChatOpenAI(
            model=deployment,
            base_url=endpoint,
            api_key=api_key,
            use_responses_api=True,
            max_retries=0,
        )

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_schema: type[StructuredModelT],
    ) -> StructuredModelT:
        """Make exactly one DTO-backed structured invocation for a domain schema."""

        binding = _FOUNDRY_BINDINGS.get(response_schema)
        if binding is None:
            raise StructuredOutputError(
                f"Microsoft Foundry has no transport DTO for {response_schema.__name__}"
            )

        structured_model = self._chat_model.with_structured_output(
            binding.transport_schema,
            method="json_schema",
            strict=True,
        )
        try:
            raw_result = await structured_model.ainvoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]
            )
            transport_result = binding.transport_schema.model_validate(raw_result)
            domain_result = binding.to_domain(transport_result)
        except (FoundryMappingError, ValidationError) as exc:
            raise StructuredOutputError(
                f"Microsoft Foundry response did not match {response_schema.__name__}: {exc}"
            ) from exc

        return cast(StructuredModelT, domain_result)
