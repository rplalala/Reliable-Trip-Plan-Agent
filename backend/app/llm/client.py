"""Provider-independent interfaces for structured LLM calls."""

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

StructuredModelT = TypeVar("StructuredModelT", bound=BaseModel)


class StructuredOutputError(RuntimeError):
    """Raised when a provider response cannot be parsed into the requested schema."""


@runtime_checkable
class StructuredLLMClient(Protocol):
    """Generate a Pydantic model without exposing provider details to callers."""

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_schema: type[StructuredModelT],
    ) -> StructuredModelT:
        """Return one provider-native structured response."""

        ...
