import { describe, expect, it } from "vitest";
import type { PlanningEvent } from "./api/planningStream";
import { advanceProgress } from "./planningProgress";

const stage = (name: string, status = "completed", occurrence = 1): PlanningEvent => ({
  type: "stage", stage: name, status, occurrence, run_id: "test", sequence: 1, elapsed_ms: 0,
});

describe("workflow position estimates", () => {
  it("advances on real stages without regressing on nested or repeated events", () => {
    const value = advanceProgress(0, stage("generation", "started"), "product");
    expect(value).toBe(0.5);
    expect(advanceProgress(value, stage("weather"), "product")).toBe(value);
    expect(advanceProgress(value, stage("generation"), "product")).toBeGreaterThan(value);
    expect(advanceProgress(value, stage("repair", "skipped"), "product")).toBe(value);
    expect(advanceProgress(value, stage("unknown"), "product")).toBe(value);
  });
  it("never treats heartbeat, errors, cancellation or terminal payloads as successful completion", () => {
    for (const type of ["started", "detail", "error", "cancelled", "result"]) {
      expect(advanceProgress(0.5, { ...stage("generation"), type }, "product")).toBe(0.5);
    }
    expect(advanceProgress(0, stage("generation", "failed"), "product")).toBe(0);
    expect(advanceProgress(0, stage("introductions"), "product")).toBeLessThan(1);
  });
  it("keeps repeated repair rounds bounded and monotonically advances", () => {
    let position = 0.77;
    for (let round = 1; round <= 20; round++) {
      const next = advanceProgress(position, stage("repair_round", "completed", round), "v3");
      expect(next).toBeGreaterThan(position);
      expect(next).toBeLessThan(0.9);
      position = next;
    }
    expect(advanceProgress(position, stage("validation"), "v3")).toBe(position);
  });
  it("uses shorter workflows for earlier versions", () => {
    expect(advanceProgress(0, stage("requirements"), "v0")).toBe(0.3);
    expect(advanceProgress(0.3, stage("generation"), "v0")).toBe(0.95);
    expect(advanceProgress(0.3, stage("weather"), "v0")).toBe(0.3);
    for (const version of ["v1", "v2"] as const) {
      expect(advanceProgress(0, stage("generation"), version)).toBeGreaterThan(0.8);
      expect(advanceProgress(0, stage("repair"), version)).toBe(0);
      expect(advanceProgress(0, stage("nearby"), version)).toBe(0.98);
    }
  });
});
