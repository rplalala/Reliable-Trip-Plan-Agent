import { requestJson } from "../../shared/api/http";
import type { DeveloperPlanningRequest } from "./types";

export function submitDeveloperPlanningRequest(
  request: DeveloperPlanningRequest,
): Promise<unknown> {
  return requestJson<unknown>("/api/dev/planning", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
