"""Independent V2 work limits; these never enlarge main or Nearby capacities."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RAGConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    version: Literal["tripworld_runtime_1"] = "tripworld_runtime_1"
    max_queries: int = Field(default=2, ge=1, le=4)
    max_positions: int = Field(default=20, ge=1, le=80)
    total_query_tokens: int = Field(default=1024, ge=1, le=2048)
    top_k: int = Field(default=10, ge=1, le=20)
    resolution_entities: int = Field(default=6, ge=0, le=16)
    details_calls: int = Field(default=8, ge=0, le=20)
    fallback_calls: int = Field(default=2, ge=0, le=4)
    radius_km: Literal[15] = 15
    identity_radius_km: Literal[1] = 1
    deadline_seconds: float = Field(default=30, gt=0, le=360)
    embedding_timeout: float = Field(default=8, gt=0, le=8)
    sql_timeout: float = Field(default=3, gt=0, le=60)
    connect_timeout: float = Field(default=2, gt=0, le=2)
    google_timeout: float = Field(default=4, gt=0, le=4)
    retries: Literal[0] = 0

    @model_validator(mode="after")
    def coordinated_limits(self):
        if self.max_queries * self.top_k > self.max_positions:
            raise ValueError("Query result positions exceed processing capacity")
        if self.max_queries * 512 > self.total_query_tokens:
            raise ValueError("Query token budget must support the configured query count")
        return self
