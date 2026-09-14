"""Microsoft Foundry implementation of the structured LLM client interface."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError

from backend.app.evidence.experience_models import ExperienceProfileDraft
from backend.app.llm.azure_foundry.dto import (
    FoundryExperienceProfileDTO,
    FoundryItineraryDTO,
    FoundryRequirementsWithNamedPlaceIntentsDTO,
    FoundryTravelRequirementsDTO,
    FoundryTripIntentExtractionDTO,
)
from backend.app.llm.azure_foundry.mapping import (
    FoundryMappingError,
    map_foundry_itinerary,
    map_foundry_requirements,
    map_foundry_requirements_with_named_places,
    map_foundry_trip_intents,
)
from backend.app.llm.azure_foundry.v1_itinerary import map_foundry_v1_itinerary
from backend.app.llm.client import StructuredModelT, StructuredOutputError
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.named_place_intent import RequirementsWithNamedPlaceIntents
from backend.app.schemas.request import TravelRequirements
from backend.app.schemas.trip_intent import TripIntentExtractionResult
from backend.app.schemas.v1_itinerary import V1Itinerary


@dataclass(frozen=True)
class _FoundryBinding:
    transport_schema: type[BaseModel]
    to_domain: Callable[[BaseModel], BaseModel]


def _map_requirements(value: BaseModel) -> TravelRequirements:
    dto = FoundryTravelRequirementsDTO.model_validate(value)
    return map_foundry_requirements(dto)


def _map_requirements_with_named_places(value: BaseModel) -> RequirementsWithNamedPlaceIntents:
    dto = FoundryRequirementsWithNamedPlaceIntentsDTO.model_validate(value)
    return map_foundry_requirements_with_named_places(dto)


def _map_trip_intents(value: BaseModel) -> TripIntentExtractionResult:
    dto = FoundryTripIntentExtractionDTO.model_validate(value)
    return map_foundry_trip_intents(dto)


def _map_itinerary(value: BaseModel) -> Itinerary:
    dto = FoundryItineraryDTO.model_validate(value)
    return map_foundry_itinerary(dto)


def _map_v1_itinerary(value: BaseModel) -> V1Itinerary:
    dto = FoundryItineraryDTO.model_validate(value)
    return map_foundry_v1_itinerary(dto)


def _map_experience_profile(value: BaseModel) -> ExperienceProfileDraft:
    dto = FoundryExperienceProfileDTO.model_validate(value)
    return ExperienceProfileDraft.model_validate(dto.model_dump())


_FOUNDRY_BINDINGS: dict[type[BaseModel], _FoundryBinding] = {
    TravelRequirements: _FoundryBinding(
        transport_schema=FoundryTravelRequirementsDTO,
        to_domain=_map_requirements,
    ),
    RequirementsWithNamedPlaceIntents: _FoundryBinding(
        transport_schema=FoundryRequirementsWithNamedPlaceIntentsDTO,
        to_domain=_map_requirements_with_named_places,
    ),
    TripIntentExtractionResult: _FoundryBinding(
        transport_schema=FoundryTripIntentExtractionDTO,
        to_domain=_map_trip_intents,
    ),
    Itinerary: _FoundryBinding(
        transport_schema=FoundryItineraryDTO,
        to_domain=_map_itinerary,
    ),
    V1Itinerary: _FoundryBinding(
        transport_schema=FoundryItineraryDTO,
        to_domain=_map_v1_itinerary,
    ),
    ExperienceProfileDraft: _FoundryBinding(
        transport_schema=FoundryExperienceProfileDTO,
        to_domain=_map_experience_profile,
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
