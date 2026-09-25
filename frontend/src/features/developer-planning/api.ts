import { requestJson } from "../../shared/api/http";
import type { DeveloperPlanningRequest } from "./types";
import { planningStream, type PlanningEvent } from "../../shared/api/planningStream";

export function submitDeveloperPlanningRequest(
  request: DeveloperPlanningRequest,
  options?: { signal: AbortSignal; onEvent: (event: PlanningEvent) => void },
): Promise<unknown> {
  if (options) return planningStream("/api/dev/planning/stream", request, options.signal, options.onEvent);
  return requestJson<unknown>("/api/dev/planning", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
