"""Provider-independent LLM interfaces and reusable provider clients."""

from backend.app.llm.client import StructuredLLMClient, StructuredOutputError


def __getattr__(name):
    """Keep domain error imports independent of provider adapter initialization."""
    if name == "AzureFoundryStructuredLLMClient":
        from backend.app.llm.azure_foundry import AzureFoundryStructuredLLMClient

        return AzureFoundryStructuredLLMClient
    raise AttributeError(name)

__all__ = [
    "AzureFoundryStructuredLLMClient",
    "StructuredLLMClient",
    "StructuredOutputError",
]
