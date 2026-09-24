"""V3-only post-primary extension of the shared tools graph."""

from backend.app.versions.v1.graph import build_tools_graph
from backend.app.versions.v3.state import V3State
from backend.app.versions.v3.wiring import V3PostPrimary, reference_node


def build_v3_graph(
    llm_client,
    evidence_service,
    tracer,
    *,
    owner,
    request_deadline,
    quantity_review_enabled=False,
    **kwargs,
):
    extension = kwargs.get("discovery_extension")
    if extension is None:
        raise ValueError("V3 requires the request discovery dependency")
    return build_tools_graph(
        llm_client,
        evidence_service,
        tracer,
        post_primary=V3PostPrimary(
            llm_client,
            evidence_service,
            tracer,
            extension,
            owner,
            request_deadline,
            quantity_review_enabled,
        ),
        reference_node=reference_node(kwargs["reference_service"], tracer, request_deadline),
        state_schema=V3State,
        graph_name="v3",
        **kwargs,
    )
