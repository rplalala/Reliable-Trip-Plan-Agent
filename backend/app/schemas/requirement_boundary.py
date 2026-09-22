"""Requirement-interface failures are not missing user information."""

from backend.app.llm.client import StructuredOutputError


class RequirementBoundaryError(StructuredOutputError):
    def __init__(
        self, code, *, stage="canonicalization", category="invalid_model_contract", errors=()
    ):
        self.code = code
        self.stage = stage
        self.category = category
        self.errors = tuple(errors)
        super().__init__(code)

    def as_dict(self):
        return {
            "status": self.category,
            "code": self.code,
            "stage": self.stage,
            "errors": self.errors,
        }
