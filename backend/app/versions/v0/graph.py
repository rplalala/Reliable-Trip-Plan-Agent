"""LangGraph definition for the V0 plain-LLM workflow."""

from collections.abc import Sequence

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from backend.app.llm.client import StructuredLLMClient
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequirements
from backend.app.versions.v0.prompts import (
    ITINERARY_GENERATION_SYSTEM_PROMPT,
    REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
    build_itinerary_generation_prompt,
    build_requirement_extraction_prompt,
)
from backend.app.versions.v0.state import V0State

REQUIRED_REQUIREMENT_FIELDS = ("destination", "start_date", "end_date")


class MissingRequiredFieldsError(RuntimeError):
    """Raised when V0 cannot plan without inventing critical user requirements."""

    def __init__(
        self,
        *,
        unresolved_fields: Sequence[str],
        requirements: TravelRequirements,
    ) -> None:
        self.unresolved_fields = tuple(unresolved_fields)
        self.requirements = requirements
        fields = ", ".join(self.unresolved_fields)
        super().__init__(f"Missing required travel fields: {fields}")


class V0StageError(RuntimeError):
    """Identify the V0 stage in which a provider or schema failure occurred."""

    def __init__(self, stage: str) -> None:
        self.stage = stage
        super().__init__(f"V0 stage failed: {stage}")


def build_v0_graph(llm_client: StructuredLLMClient) -> CompiledStateGraph:
    """Build the fixed two-node V0 graph without tools or persistence."""

    async def extract_requirements(state: V0State) -> dict[str, TravelRequirements]:
        try:
            requirements = await llm_client.generate_structured(
                system_prompt=REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
                user_prompt=build_requirement_extraction_prompt(
                    state["request"],
                    state["reference_date"],
                ),
                response_schema=TravelRequirements,
            )
        except Exception as exc:
            raise V0StageError("extract_requirements") from exc

        missing_fields = [
            field_name
            for field_name in REQUIRED_REQUIREMENT_FIELDS
            if getattr(requirements, field_name) is None
        ]
        if missing_fields:
            unresolved_fields = list(
                dict.fromkeys([*requirements.unresolved_fields, *missing_fields])
            )
            requirements = requirements.model_copy(
                update={"unresolved_fields": unresolved_fields}
            )
            raise MissingRequiredFieldsError(
                unresolved_fields=missing_fields,
                requirements=requirements,
            )

        return {"requirements": requirements}

    async def generate_itinerary(state: V0State) -> dict[str, Itinerary]:
        requirements = state["requirements"]
        try:
            itinerary = await llm_client.generate_structured(
                system_prompt=ITINERARY_GENERATION_SYSTEM_PROMPT,
                user_prompt=build_itinerary_generation_prompt(
                    state["request"],
                    requirements,
                    state["reference_date"],
                ),
                response_schema=Itinerary,
            )
        except Exception as exc:
            raise V0StageError("generate_itinerary") from exc

        return {"itinerary": itinerary}

    graph_builder = StateGraph(V0State)
    graph_builder.add_node("extract_requirements", extract_requirements)
    graph_builder.add_node("generate_itinerary", generate_itinerary)
    graph_builder.add_edge(START, "extract_requirements")
    graph_builder.add_edge("extract_requirements", "generate_itinerary")
    graph_builder.add_edge("generate_itinerary", END)
    return graph_builder.compile(name="v0")
