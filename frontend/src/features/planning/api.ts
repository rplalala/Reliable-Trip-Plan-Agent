import { requestJson } from "../../shared/api/http";
import type { ProductPlanningInput, ProductPlanningResponse } from "./types";
import { planningStream, type PlanningEvent } from "../../shared/api/planningStream";

export function submitPlanningRequest(
  input: ProductPlanningInput,
  options?: { signal: AbortSignal; onEvent: (event: PlanningEvent) => void },
): Promise<ProductPlanningResponse> {
  if (options) return planningStream("/api/planning/stream", input, options.signal, options.onEvent);
  return requestJson<ProductPlanningResponse>("/api/planning", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function getTripDateWindow(): Promise<import("./datePolicy").TripDateWindow> {
  return requestJson("/api/planning/date-window", { method: "GET", cache: "no-store" });
}
