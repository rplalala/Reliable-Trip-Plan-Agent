import { afterEach, describe, expect, it, vi } from "vitest";

import { getDestinationSuggestions, submitPlanningRequest } from "./api";

describe("product planning API", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("encodes only the typed prefix for the destination proxy", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200,
      json: () => Promise.resolve({ source: "geodb", suggestions: [] }) });
    vi.stubGlobal("fetch", fetchMock);
    const signal = new AbortController().signal;
    await getDestinationSuggestions("New & York", signal);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("/api/input-assistance/destinations?q=New%20%26%20York");
    expect(init.signal).toBe(signal);
    expect(init.body).toBeUndefined();
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

  it.each([false, true])("preserves public completion fields (stream=%s)", async (stream) => {
    const result = {
      status: "completed",
      requirements: { destination: "Kyoto" },
      itinerary: { destination: "Kyoto", days: [] },
      minimum_daily_coverage: { status: "satisfied" },
      policy_completion: "incomplete",
      policy_reasons: ["required_visit_obligation_unmet"],
    };
    const fetchMock = vi.fn().mockResolvedValue(new Response(
      stream ? `data: ${JSON.stringify({ type: "result", run_id: "test-run", sequence: 1, elapsed_ms: 1, result })}\n\n` : JSON.stringify(result),
      { headers: { "Content-Type": stream ? "text/event-stream" : "application/json" } },
    ));
    vi.stubGlobal("fetch", fetchMock);
    const response = await submitPlanningRequest({
      destination: "Kyoto", start_date: "2026-09-12", end_date: "2026-09-12",
      traveler_count: 1, budget: { amount: "2000", currency: "AUD" },
    }, stream ? { signal: new AbortController().signal, onEvent: vi.fn() } : undefined);

    expect(response).toEqual(result);
    expect(fetchMock.mock.calls[0][0]).toBe(stream ? "/api/planning/stream" : "/api/planning");
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
      budget: { amount: "2000", currency: "AUD" },
    });

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    const payload = JSON.parse(String(init.body)) as Record<string, unknown>;
    expect(payload.budget).toEqual({ amount: "2000", currency: "AUD" });
    expect(payload).not.toHaveProperty("additional_preferences");
  });
});
