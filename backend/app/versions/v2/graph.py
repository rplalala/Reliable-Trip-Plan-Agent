"""Explicit V2 graph injection; common tools nodes are not copied."""

from backend.app.versions.v1.graph import build_tools_graph


def build_v2_graph(llm_client, evidence_service, tracer, *, discovery_extension, **kwargs):
    return build_tools_graph(
        llm_client, evidence_service, tracer, discovery_extension=discovery_extension, **kwargs
    )
