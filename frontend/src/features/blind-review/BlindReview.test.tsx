import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import { BlindReview } from "./BlindReview";
import type { Presentation } from "./answers";

const presentation: Presentation = {
  schema_version: "rtpeval_human_package_1", batch_id: "1".repeat(32), batch_revision: 1,
  presentation_id: "2".repeat(32), presentation_hash: "4".repeat(64), rater_ref: "3".repeat(32),
  dimensions: ["preference", "pace", "usefulness"],
  tasks: [{ task_id: "task-1", input: { destination: "Example City", additional_preferences: "Prefer architecture" },
    plans: Object.fromEntries(["A", "B", "C", "D"].map(label => [label, { days: [{ date: "2020-01-01", items: [{
      kind: "activity", fields: { title: "Museum <script>ignored</script>", notes: "Time uncertain" }, notices: [],
    }] }] }])) }],
};

it("rater can submit ties, resume and correct an answer", () => {
  const storage = new Map<string, string>();
  const persistence = { getItem: (key: string) => storage.get(key) ?? null, setItem: (key: string, value: string) => { storage.set(key, value); } };
  const first = render(<BlindReview presentation={presentation} storage={persistence} />);
  expect(screen.getAllByText("Museum <script>ignored</script>")).toHaveLength(4);
  expect(screen.getByRole("button", { name: "Submit answer" })).toBeDisabled();
  for (const d of presentation.dimensions) {
    for (const label of ["A", "B", "C", "D"]) {
      fireEvent.change(screen.getByLabelText(`${d}: position for ${label}`), { target: { value: label === "D" ? "2" : "1" } });
    }
  }
  fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
  expect(screen.getByText("Submitted revision 1")).toBeInTheDocument();
  first.unmount();
  render(<BlindReview presentation={presentation} storage={persistence} />);
  expect(screen.getByText("Submitted revision 1")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Asia/Shanghai" } });
  expect(screen.getByText("Submitted revision 1")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("pace: response"), { target: { value: "unable_to_judge" } });
  fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
  expect(screen.getByText("Submitted revision 2")).toBeInTheDocument();
  const saved = JSON.parse([...storage.values()][0]);
  expect(saved.answers).toHaveLength(2);
  expect(saved.answers[1].presentation_hash).toBe(presentation.presentation_hash);
  expect(saved.answers[1]).not.toHaveProperty("time_zone");
  expect(saved.answers[1].responses.pace).toEqual({ status: "unable_to_judge" });
});

it("storage failure is visible and downloadable answers remain available", () => {
  render(<BlindReview presentation={presentation} storage={{ getItem: () => null, setItem: vi.fn(() => { throw Error("Denied"); }) }} />);
  fireEvent.click(screen.getByRole("button", { name: "Save draft" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Local save failed");
  expect(screen.getByRole("button", { name: "Download answers JSON" })).toBeEnabled();
});

it("travel rows show inferred arrival without uncertainty fields or notice blocks", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "travel", fields: {
    departure_time: "2020-01-01T10:00:00+00:00", duration_seconds: 1800,
    inferred_arrival: "2020-01-01T10:30:00+00:00",
    unknowns: "Travel time uncertain",
  }, notices: ["Arrival not supplied; inferred time is display arithmetic only"] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  expect(screen.getByText("Travel")).toBeInTheDocument();
  expect(screen.getByText("Inferred arrival")).toBeInTheDocument();
  expect(screen.getByText("Travel duration (seconds)")).toBeInTheDocument();
  expect(screen.getByText("2020-01-01 10:30")).toBeInTheDocument();
  expect(screen.queryByText("Uncertainty")).not.toBeInTheDocument();
  expect(screen.queryByText("Travel time uncertain")).not.toBeInTheDocument();
  expect(screen.queryByText("Arrival not supplied; inferred time is display arithmetic only")).not.toBeInTheDocument();
});

it("rater can choose a time zone and see converted clocks and cross-day dates", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "activity", fields: {
    start_time: "2020-01-01T23:30:00+02:00", end_time: "2020-01-02T00:00:00+02:00",
  }, notices: [] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  expect(screen.getByLabelText("Time zone")).toHaveValue("UTC");
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2020-01-01 21:30")).toBeInTheDocument();
  expect(plan.getByText("2020-01-01 22:00")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Asia/Shanghai" } });
  expect(plan.getByText("2020-01-02 05:30")).toBeInTheDocument();
  expect(plan.getByText("2020-01-02 06:00")).toBeInTheDocument();
  expect(plan.getByText("Source day: 2020-01-01")).toBeInTheDocument();
  expect(material.tasks[0].plans.A.days[0].items[0].fields.start_time).toBe("2020-01-01T23:30:00+02:00");
});

it("selected time zone handles daylight saving for departure and inferred arrival", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "travel", fields: {
    departure_time: "2024-03-10T06:30:00Z", inferred_arrival: "2024-03-10T07:30:00Z",
  }, notices: ["Arrival not supplied; inferred time is display arithmetic only"] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "America/New_York" } });
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2024-03-10 01:30")).toBeInTheDocument();
  expect(plan.getByText("2024-03-10 03:30")).toBeInTheDocument();
  expect(plan.getByText("Inferred arrival")).toBeInTheDocument();
  expect(plan.queryByText("Arrival not supplied; inferred time is display arithmetic only")).not.toBeInTheDocument();
});

it("missing zones and invalid timestamps remain explicit without invented conversion", () => {
  const material = structuredClone(presentation);
  material.tasks[0].input.start_date = "2024-03-10";
  material.tasks[0].plans.A.days[0].items = [{ kind: "activity", fields: {
    start_time: "2024-03-10T09:15:00", end_time: "10:20",
  }, notices: [] }, { kind: "travel", fields: {
    departure_time: "2024-02-30T10:00:00Z", arrival_time: "25:70", inferred_arrival: null,
  }, notices: [] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Australia/Sydney" } });
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2024-03-10 09:15")).toBeInTheDocument();
  expect(plan.getByText("10:20")).toBeInTheDocument();
  expect(plan.queryByText("Time zone not supplied; not converted")).not.toBeInTheDocument();
  expect(plan.queryByText("Time unavailable for conversion; original value retained")).not.toBeInTheDocument();
  expect(plan.getByText("2024-02-30T10:00:00Z")).toBeInTheDocument();
  expect(plan.getByText("25:70")).toBeInTheDocument();
  expect(plan.getByText("Not supplied")).toBeInTheDocument();
  expect(within(screen.getByRole("region", { name: "Original request" })).getByText("2024-03-10")).toBeInTheDocument();
});

it("midnight uses zero hours and fractional-offset zones retain minutes", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "activity", fields: {
    start_time: "2024-01-02T00:00:00Z", end_time: "2024-01-02T00:30:00Z",
  }, notices: [] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2024-01-02 00:00")).toBeInTheDocument();
  const india = screen.getByRole("option", { name: /^Asia\/(Kolkata|Calcutta)$/ }) as HTMLOptionElement;
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: india.value } });
  expect(plan.getByText("2024-01-02 05:30")).toBeInTheDocument();
  expect(plan.getByText("2024-01-02 06:00")).toBeInTheDocument();
});

it("explicit offsets convert without exposing an original timestamp control", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "activity", fields: {
    start_time: "2024-01-01T23:30:00+0200", end_time: "2024-01-02T00:00:00+02",
  }, notices: [] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Asia/Shanghai" } });
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2024-01-02 05:30")).toBeInTheDocument();
  expect(plan.getByText("2024-01-02 06:00")).toBeInTheDocument();
  expect(screen.queryAllByText("Original timestamp")).toHaveLength(0);
  expect(plan.queryByText("2024-01-01T23:30:00+0200")).not.toBeInTheDocument();
  expect(plan.queryByText("2024-01-02T00:00:00+02")).not.toBeInTheDocument();
});

it("clearing requires confirmation and resets only this review package", () => {
  const storage = new Map<string, string>([["another-package", "other answers"]]);
  const persistence = { getItem: (key: string) => storage.get(key) ?? null, setItem: (key: string, value: string) => { storage.set(key, value); } };
  const material = structuredClone(presentation);
  material.tasks.push({ ...structuredClone(material.tasks[0]), task_id: "task-2" });
  const first = render(<BlindReview presentation={material} storage={persistence} />);
  for (const d of material.dimensions) fireEvent.change(screen.getByLabelText(`${d}: response`), { target: { value: "unable_to_judge" } });
  fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
  fireEvent.click(screen.getByRole("button", { name: "Next task" }));
  fireEvent.change(screen.getByLabelText("pace: reason"), { target: { value: "Unsaved note" } });
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Asia/Shanghai" } });
  fireEvent.click(screen.getByRole("button", { name: "Clear answers" }));
  expect(screen.getByText(/Download a JSON backup first/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Cancel clear" }));
  expect(screen.getByLabelText("pace: reason")).toHaveValue("Unsaved note");
  expect(screen.getByText("Task 2 of 2")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Clear answers" }));
  fireEvent.click(screen.getByRole("button", { name: "Confirm clear" }));
  expect(screen.getByText("Task 1 of 2")).toBeInTheDocument();
  expect(screen.queryByText("Submitted revision 1")).not.toBeInTheDocument();
  expect(screen.getByLabelText("pace: reason")).toHaveValue("");
  expect(screen.getByRole("button", { name: "Submit answer" })).toBeDisabled();
  expect(screen.getByLabelText("Time zone")).toHaveValue("Asia/Shanghai");
  expect(storage.get("another-package")).toBe("other answers");
  first.unmount();
  render(<BlindReview presentation={material} storage={persistence} />);
  expect(screen.queryByText("Submitted revision 1")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Submit answer" })).toBeDisabled();
});

it("failed local clearing preserves submitted answers and unsaved edits", () => {
  const storage = new Map<string, string>();
  let denied = false;
  const persistence = { getItem: (key: string) => storage.get(key) ?? null, setItem: (key: string, value: string) => {
    if (denied) throw Error("Denied"); storage.set(key, value);
  } };
  render(<BlindReview presentation={presentation} storage={persistence} />);
  for (const d of presentation.dimensions) fireEvent.change(screen.getByLabelText(`${d}: response`), { target: { value: "not_applicable" } });
  fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
  const saved = [...storage.values()];
  fireEvent.change(screen.getByLabelText("pace: reason"), { target: { value: "Keep this unsaved edit" } });
  denied = true;
  fireEvent.click(screen.getByRole("button", { name: "Clear answers" }));
  fireEvent.click(screen.getByRole("button", { name: "Confirm clear" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Local clear failed. Answers are unchanged");
  expect(screen.getByText("Submitted revision 1")).toBeInTheDocument();
  expect(screen.getByLabelText("pace: reason")).toHaveValue("Keep this unsaved edit");
  expect(screen.getByRole("button", { name: "Download answers JSON" })).toBeEnabled();
  expect([...storage.values()]).toEqual(saved);
});

it("downloaded JSON restores submitted and draft revisions after confirmed clearing", async () => {
  const storage = new Map<string, string>();
  const persistence = { getItem: (key: string) => storage.get(key) ?? null, setItem: (key: string, value: string) => { storage.set(key, value); } };
  let backup: Blob | undefined;
  vi.stubGlobal("URL", { createObjectURL: (blob: Blob) => { backup = blob; return "blob:backup"; }, revokeObjectURL: () => {} });
  const click = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
  try {
    render(<BlindReview presentation={presentation} storage={persistence} />);
    for (const d of presentation.dimensions) fireEvent.change(screen.getByLabelText(`${d}: response`), { target: { value: "unable_to_judge" } });
    fireEvent.click(screen.getByRole("button", { name: "Save draft" }));
    fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
    fireEvent.click(screen.getByRole("button", { name: "Download answers JSON" }));
    expect(click).toHaveBeenCalledOnce();
    const text = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader(); reader.onload = () => resolve(String(reader.result)); reader.onerror = () => reject(Error("Read failed"));
      reader.readAsText(backup!);
    });
    const original = JSON.parse(text);
    expect(original.answers.map((a: { answer_revision: number; state: string }) => [a.answer_revision, a.state])).toEqual([[1, "draft"], [2, "submitted"]]);
    fireEvent.click(screen.getByRole("button", { name: "Clear answers" }));
    fireEvent.click(screen.getByRole("button", { name: "Confirm clear" }));
    expect(screen.queryByText("Submitted revision 2")).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Import answers JSON"), { target: { files: [new File([text], "answers.json", { type: "application/json" })] } });
    await waitFor(() => expect(screen.getByText("Submitted revision 2")).toBeInTheDocument());
    expect(JSON.parse([...storage.values()][0])).toEqual(original);
    expect(screen.getByLabelText("pace: response")).toHaveValue("unable_to_judge");
  } finally { click.mockRestore(); vi.unstubAllGlobals(); }
});

it("successful clearing invalidates an import that has not finished reading", async () => {
  const storage = new Map<string, string>();
  const persistence = { getItem: (key: string) => storage.get(key) ?? null, setItem: (key: string, value: string) => { storage.set(key, value); } };
  let finishRead: (() => void) | undefined;
  let backup = "";
  vi.stubGlobal("FileReader", class {
    result: string | null = null;
    onload: (() => void) | null = null;
    onerror: (() => void) | null = null;
    readAsText() { finishRead = () => { this.result = backup; this.onload?.(); }; }
  });
  try {
    render(<BlindReview presentation={presentation} storage={persistence} />);
    for (const d of presentation.dimensions) fireEvent.change(screen.getByLabelText(`${d}: response`), { target: { value: "not_applicable" } });
    fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
    backup = [...storage.values()][0];
    fireEvent.change(screen.getByLabelText("Import answers JSON"), { target: { files: [new File([backup], "answers.json")] } });
    fireEvent.click(screen.getByRole("button", { name: "Clear answers" }));
    fireEvent.click(screen.getByRole("button", { name: "Confirm clear" }));
    await act(async () => { finishRead!(); await Promise.resolve(); });
    expect(screen.queryByText("Submitted revision 1")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Submit answer" })).toBeDisabled();
    expect(JSON.parse([...storage.values()][0]).answers).toEqual([]);
    expect(screen.getByRole("status")).toHaveTextContent("Answers cleared");
  } finally { vi.unstubAllGlobals(); }
});
