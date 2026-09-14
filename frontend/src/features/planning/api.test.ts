import { afterEach, describe, expect, it, vi } from "vitest";

import { submitPlanningRequest } from "./api";

describe("product planning API", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("submits a version-agnostic product payload", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () =>
        Promise.resolve({
          status: "needs_clarification",
          requirements: { unresolved_fields: ["start_date"] },
        }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await submitPlanningRequest({
      destination: "Beijing",
      start_date: "2026-09-12",
      end_date: "2026-09-14",
      traveler_count: 2,
      budget: { amount: "2000", currency: "AUD" },
      additional_preferences: "Local food and quiet mornings.",
    });

    expect(fetchMock).toHaveBeenCalledOnce();
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    const payload = JSON.parse(String(init.body)) as Record<string, unknown>;
    expect(url).toBe("/api/planning");
    expect(payload.destination).toBe("Beijing");
    expect(payload.start_date).toBe("2026-09-12");
    expect(payload.end_date).toBe("2026-09-14");
    expect(payload.traveler_count).toBe(2);
    expect(payload.budget).toEqual({ amount: "2000", currency: "AUD" });
    expect(payload.additional_preferences).toBe("Local food and quiet mornings.");
    expect(payload).not.toHaveProperty("reference_date");
    expect(payload).not.toHaveProperty("request_text");
    expect(payload).not.toHaveProperty("version");
  });

  it("omits optional fields when the user did not supply them", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ status: "completed" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await submitPlanningRequest({
      destination: "Beijing",
      start_date: "2026-09-12",
      end_date: "2026-09-14",
      traveler_count: 2,
    });

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    const payload = JSON.parse(String(init.body)) as Record<string, unknown>;
    expect(payload).not.toHaveProperty("budget");
    expect(payload).not.toHaveProperty("additional_preferences");
  });
});
