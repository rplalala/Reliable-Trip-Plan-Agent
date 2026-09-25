import type { ProductPlanningInput } from "../planning/types";

export type DeveloperVersion = "v0" | "v1" | "v2" | "v3";

export interface DeveloperPlanningRequest {
  version: DeveloperVersion;
  request: ProductPlanningInput;
  reference_date: string;
}
