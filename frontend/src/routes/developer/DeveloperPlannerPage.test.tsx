import { act, fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { submitDeveloperPlanningRequest } from "../../features/developer-planning/api";
import { DeveloperPlannerPage } from "./DeveloperPlannerPage";

vi.mock("../../features/developer-planning/api", () => ({ submitDeveloperPlanningRequest: vi.fn() }));
vi.mock("../../features/planning/api", () => ({
  getTripDateWindow: vi.fn().mockResolvedValue({ allowedStart: "2026-09-11", allowedEnd: "2026-09-24", maxTripDays: 10 }),
}));
const submit = vi.mocked(submitDeveloperPlanningRequest);
const panel = (version: string) => within(screen.getByRole("region", { name: `${version} run` }));
async function launch() {
  const view = render(<DeveloperPlannerPage />);
  await act(async () => {});
  for (const [label, value] of Object.entries({ Destination: "Kyoto", "Start date": "2026-09-12", "End date": "2026-09-12", Travelers: "2", "Budget amount": "2000", Currency: "AUD" })) {
    fireEvent.change(screen.getByLabelText(label), { target: { value } });
  }
  fireEvent.click(screen.getByRole("button", { name: "Run all versions" }));
  return view;
}
describe("four independent research runs", () => {
  beforeEach(() => { submit.mockReset(); });
  it("displays multiple repair rounds, targets and revalidation without mixing versions", async () => {
    submit.mockImplementation(() => new Promise(() => {}));
    await launch();
    act(() => {
      const emit = submit.mock.calls[3][1]!.onEvent;
      for (const round of [1, 2]) {
        emit({ type: "stage", run_id: "repair", sequence: round * 3, elapsed_ms: round * 1000,
          stage: "repair_round", occurrence: round, status: "completed", duration_ms: round * 250 });
        emit({ type: "detail", run_id: "repair", sequence: round * 3 + 1, elapsed_ms: round * 1000,
          name: "repair_targets", stage_id: `repair_round:${round}`, details: { target_ids: [`issue-${round}`] } });
        emit({ type: "stage", run_id: "repair", sequence: round * 3 + 2, elapsed_ms: round * 1000,
          stage: "revalidation", occurrence: round, parent_id: `repair_round:${round}`,
          status: "completed", duration_ms: 100 });
      }
    });
    fireEvent.click(panel("V3").getByText("Mechanism progress and timings"));
    expect(panel("V3").getByText(/repair_round #1: completed · 0.25 s/)).toBeVisible();
    expect(panel("V3").getByText(/repair_round #2: completed · 0.50 s/)).toBeVisible();
    expect(panel("V3").getByText(/revalidation #2: completed · 0.10 s/)).toBeVisible();
    expect(panel("V3").getByText(/"issue-2"/)).toBeVisible();
    expect(panel("V0").queryByText(/repair_round/)).not.toBeInTheDocument();
    expect(panel("V3").getByRole("status")).toHaveTextContent("running");
  });
  it("starts all four from one snapshot, isolates failures and displays stage timing", async () => {
    const resolve: Array<(value: unknown) => void> = [];
    const reject: Array<(value: unknown) => void> = [];
    submit.mockImplementation(() => new Promise((yes, no) => { resolve.push(yes); reject.push(no); }));
    await launch();
    expect(submit.mock.calls.map(([request]) => request.version)).toEqual(["v0", "v1", "v2", "v3"]);
    expect(new Set(submit.mock.calls.map(([, options]) => options?.signal)).size).toBe(4);
    expect(screen.getByLabelText("Destination")).toBeDisabled();
    expect(screen.getByLabelText("Reference date")).toBeDisabled();
    expect(screen.getAllByRole("progressbar")).toHaveLength(4);
    for (const [request] of submit.mock.calls) {
      expect(request.request.budget).toEqual({ amount: "2000", currency: "AUD" });
      expect(request.reference_date).toBe("2026-09-11");
      expect(request).not.toHaveProperty("request_text");
    }
    await act(async () => {
      submit.mock.calls[3][1]?.onEvent({ type: "stage", run_id: "four", sequence: 1, elapsed_ms: 500, stage: "repair_round", occurrence: 2, status: "completed", duration_ms: 420, details: { repair_status: "SKIPPED" } });
      reject[0](new Error("failed")); resolve[1]({ system_version: "v1" });
    });
    expect(panel("V0").getByRole("status")).toHaveTextContent("failed");
    expect(panel("V1").getByRole("status")).toHaveTextContent("completed");
    expect(panel("V1").getByRole("progressbar")).toHaveAttribute("aria-valuenow", "1");
    expect(panel("V2").getByRole("status")).toHaveTextContent("running");
    expect(panel("V3").getByText(/repair_round #2: completed · 0.42 s/)).toBeInTheDocument();
    expect(panel("V3").getByText(/SKIPPED/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Stop V2" }));
    expect(submit.mock.calls[2][1]?.signal.aborted).toBe(true);
    expect(submit.mock.calls[3][1]?.signal.aborted).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: "Stop all" }));
    expect(Number(panel("V3").getByRole("progressbar").getAttribute("aria-valuenow"))).toBeGreaterThan(0.77);
    expect(screen.getByLabelText("Destination")).toBeEnabled();
    await act(async () => { resolve[2]({ stale: true }); resolve[3]({ stale: true }); });
    expect(screen.queryByText(/"stale"/)).not.toBeInTheDocument();
  });
  it("reruns one version using the snapshot and ignores old events", async () => {
    submit.mockImplementation(() => new Promise(() => {}));
    await launch();
    const old = submit.mock.calls[0][1];
    fireEvent.click(screen.getByRole("button", { name: "Stop V0" }));
    fireEvent.click(screen.getByRole("button", { name: "Rerun V0" }));
    expect(submit).toHaveBeenCalledTimes(5);
    expect(panel("V0").getByRole("progressbar")).toHaveAttribute("aria-valuenow", "0");
    expect(submit.mock.calls[4][0]).toEqual(submit.mock.calls[0][0]);
    act(() => old?.onEvent({ type: "stage", run_id: "old", sequence: 9, elapsed_ms: 100, stage: "stale" }));
    expect(panel("V0").queryByText(/stale/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Stop all" }));
    fireEvent.change(screen.getByLabelText("Destination"), { target: { value: "Paris" } });
    expect(screen.queryByRole("button", { name: "Rerun V0" })).toBeNull();
  });
  it("aborts all active connections on unmount", async () => {
    submit.mockImplementation(() => new Promise(() => {}));
    const { unmount } = await launch();
    unmount();
    expect(submit).toHaveBeenCalledTimes(4);
    expect(submit.mock.calls.every(([, options]) => options?.signal.aborted)).toBe(true);
  });

  it("keeps backend cancellation distinct from failure", async () => {
    submit.mockRejectedValue(new DOMException("Cancelled", "AbortError"));
    await launch();
    await act(async () => {});
    expect(panel("V0").getByRole("status")).toHaveTextContent("cancelled");
    expect(screen.queryByText(/developer_request_failed/)).toBeNull();
  });

  it("uses the explicit research reference date for form bounds", async () => {
    submit.mockImplementation(() => new Promise(() => {}));
    await launch();
    fireEvent.click(screen.getByRole("button", { name: "Stop all" }));
    fireEvent.change(screen.getByLabelText("Reference date"), { target: { value: "2026-10-01" } });
    expect(screen.getByLabelText("Start date")).toHaveAttribute("min", "2026-10-01");
    expect(screen.getByLabelText("Start date")).toHaveAttribute("max", "2026-10-14");
    expect(screen.getByRole("button", { name: "Run all versions" })).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Start date"), { target: { value: "2026-10-01" } });
    fireEvent.change(screen.getByLabelText("End date"), { target: { value: "2026-10-01" } });
    expect(screen.getByRole("button", { name: "Run all versions" })).toBeEnabled();
  });

  it("does not mix a stopped group's events into a new input group and reports event loss", async () => {
    submit.mockImplementation(() => new Promise(() => {}));
    await launch();
    const old = submit.mock.calls[0][1]!;
    fireEvent.click(screen.getByRole("button", { name: "Stop all" }));
    fireEvent.change(screen.getByLabelText("Destination"), { target: { value: "Paris" } });
    fireEvent.click(screen.getByRole("button", { name: "Run all versions" }));
    expect(submit.mock.calls[4][0].request.destination).toBe("Paris");
    act(() => {
      old.onEvent({ type: "stage", run_id: "old", sequence: 99, elapsed_ms: 100, stage: "stale" });
      submit.mock.calls[4][1]!.onEvent({ type: "stage", run_id: "new", sequence: 3, elapsed_ms: 500,
        stage: "requirements", status: "skipped", dropped_events: 2 });
    });
    expect(panel("V0").queryByText(/stale/)).toBeNull();
    expect(panel("V0").getByRole("note")).toHaveTextContent("2 earlier events were omitted");
    expect(panel("V0").getByText("requirements : skipped")).not.toHaveTextContent("0.00 s");
  });
});
