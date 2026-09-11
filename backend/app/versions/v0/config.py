"""Environment-backed configuration for the V0 runtime."""

from pydantic import AnyHttpUrl, Field, SecretStr

from backend.app.runtime.settings import RuntimeSettings


class V0Settings(RuntimeSettings):
    """Configuration required to run V0 through Microsoft Foundry."""

    llm_model: str = Field(
        min_length=1,
        validation_alias="LLM_MODEL",
    )
    azure_openai_endpoint: AnyHttpUrl = Field(
        validation_alias="AZURE_OPENAI_ENDPOINT",
    )
    azure_openai_deployment: str = Field(
        min_length=1,
        validation_alias="AZURE_OPENAI_DEPLOYMENT",
    )
    azure_openai_api_key: SecretStr = Field(
        min_length=1,
        validation_alias="AZURE_OPENAI_API_KEY",
    )
