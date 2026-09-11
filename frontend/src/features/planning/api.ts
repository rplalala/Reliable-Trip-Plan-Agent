import { requestJson } from "../../shared/api/http";
import type { ProductPlanningInput, ProductPlanningResponse } from "./types";

export function getBrowserLocalDate(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function submitPlanningRequest(
  input: ProductPlanningInput,
): Promise<ProductPlanningResponse> {
  return requestJson<ProductPlanningResponse>("/api/planning", {
    method: "POST",
    body: JSON.stringify({
      ...input,
      reference_date: getBrowserLocalDate(),
    }),
  });
}
