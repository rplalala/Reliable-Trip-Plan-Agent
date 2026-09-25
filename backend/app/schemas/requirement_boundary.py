"""Requirement-interface failures are not missing user information."""

from backend.app.llm.client import StructuredOutputError


class RequirementBoundaryError(StructuredOutputError):
    def __init__(
        self, code, *, stage="canonicalization", category="invalid_model_contract", errors=(),
        provider_diagnostics=None
    ):
        # Internal only: as_dict remains safe for existing public API mappings.
        self.provider_diagnostics = provider_diagnostics
        self.code = code
        self.stage = stage
        self.category = category
        self.errors = tuple(errors)
        super().__init__(code)

    @property
    def provider_content_filtered(self):
        return (
            self.category == "provider_request_rejected"
            and (self.provider_diagnostics or {}).get("provider_error_code") == "content_filter"
        )

    def public_provider_action(self):
        """Provider rejection is not a successful domain input classification."""
        return {
            "message": "Your preference input triggered the AI provider's content filter. "
                       "We could not complete the preference assessment.",
            "action": ("Please rewrite your preferences as travel-related requests "
                       "and submit again."),
        }

    def as_dict(self):
        result = {
            "status": self.category,
            "code": self.code,
            "stage": self.stage,
            "errors": self.errors,
        }

        if self.provider_content_filtered:
            result.update(self.public_provider_action())
        return result
