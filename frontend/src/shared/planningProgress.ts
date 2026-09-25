import type { PlanningEvent } from "./api/planningStream";

export type ProgressProfile = "product" | "v0" | "v1" | "v2" | "v3";
type Range = readonly [number, number];

// Workflow positions, not elapsed-time predictions or measured work percentages.
const stages: Record<string, Range> = {
  requirements: [0.02, 0.12], destination: [0.12, 0.17],
  candidates: [0.17, 0.32], retrieval: [0.2, 0.28],
  weather: [0.32, 0.38], routes: [0.38, 0.46],
  official_information: [0.46, 0.5], generation: [0.5, 0.68],
  date_validation: [0.68, 0.7], transfers: [0.7, 0.73],
  validation: [0.73, 0.77], repair: [0.77, 0.9],
  nearby: [0.9, 0.95], introductions: [0.95, 0.98],
};

export function advanceProgress(previous: number, event: PlanningEvent, profile: ProgressProfile): number {
  if (event.type !== "stage" || !event.stage || !["started", "completed"].includes(event.status ?? "")) return previous;
  let range: Range | undefined = stages[event.stage];
  if (["repair_round", "repair_preparation", "repair_model", "revalidation"].includes(event.stage)) {
    // Repeated rounds advance within a bounded repair region without assuming a round limit.
    const parentRound = event.parent_id?.match(/^repair_round:(\d+)$/)?.[1];
    const round = Math.max(1, Number(parentRound ?? event.occurrence ?? 1));
    const start = 0.77 + 0.12 * (1 - 1 / round);
    const end = 0.77 + 0.12 * (1 - 1 / (round + 1));
    range = [start, end];
  }
  if (profile === "v0") {
    range = ({ requirements: [0.02, 0.3], generation: [0.3, 0.95] } as Record<string, Range>)[event.stage];
  } else if (profile === "v1" || profile === "v2") {
    if (event.stage === "nearby") range = [0.92, 0.98];
    else if (range && range[1] <= 0.73) range = [range[0] * 1.25, range[1] * 1.25];
    else range = undefined;
  }
  if (!range) return previous;
  return Math.max(previous, Math.min(0.98, range[event.status === "started" ? 0 : 1]));
}
