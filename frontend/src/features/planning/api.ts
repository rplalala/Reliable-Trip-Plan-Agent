import { requestJson } from "../../shared/api/http";
import type { ProductPlanningInput, ProductPlanningResponse } from "./types";

export function submitPlanningRequest(
  input: ProductPlanningInput,
): Promise<ProductPlanningResponse> {
  return requestJson<ProductPlanningResponse>("/api/planning", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
