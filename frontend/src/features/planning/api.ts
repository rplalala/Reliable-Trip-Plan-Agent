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

export interface DestinationSuggestion {
  id: string;
  city: string;
  region: string | null;
  country: string;
  country_code: string;
  label: string;
}

export interface DestinationSuggestionsResponse {
  source: "geodb";
  suggestions: DestinationSuggestion[];
}

export function getDestinationSuggestions(q: string, signal: AbortSignal): Promise<DestinationSuggestionsResponse> {
  return requestJson(`/api/input-assistance/destinations?q=${encodeURIComponent(q)}`,
    { method: "GET", cache: "no-store", signal });
}

export interface PreferencePolishContext {
  destination?: string;
  start_date?: string;
  end_date?: string;
  traveler_count?: number;
  budget?: { amount: string; currency: string };
}

export interface PreferencePolishRequest {
  original_text: string;
  context: PreferencePolishContext;
  client_revision: string;
}

export interface PreferencePolishResponse {
  status: "suggested" | "unchanged" | "needs_input";
  original_text: string;
  suggested_text: string | null;
  explanation: string;
  questions: string[];
  client_revision: string;
}

export function postPreferencePolish(
  request: PreferencePolishRequest,
  signal: AbortSignal,
): Promise<PreferencePolishResponse> {
  return requestJson("/api/input-assistance/preferences/polish", {
    method: "POST",
    body: JSON.stringify(request),
    signal,
  });
}
