import { fireEvent, render, screen, within } from "@testing-library/react";
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

it("travel rows use a neutral heading and explicitly labelled inferred arrival", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "travel", fields: {
    departure_time: "2020-01-01T10:00:00+00:00", duration_seconds: 1800,
    inferred_arrival: "2020-01-01T10:30:00+00:00",
  }, notices: ["Arrival not supplied; inferred time is display arithmetic only"] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  expect(screen.getByText("Travel")).toBeInTheDocument();
  expect(screen.getByText("Inferred arrival")).toBeInTheDocument();
  expect(screen.getByText("Travel duration (seconds)")).toBeInTheDocument();
  expect(screen.getByText("2020-01-01 10-30")).toBeInTheDocument();
});

it("rater can choose a time zone and see converted clocks and cross-day dates", () => {
  const material = structuredClone(presentation);
  material.tasks[0].plans.A.days[0].items = [{ kind: "activity", fields: {
    start_time: "2020-01-01T23:30:00+02:00", end_time: "2020-01-02T00:00:00+02:00",
  }, notices: [] }];
  render(<BlindReview presentation={material} storage={{ getItem: () => null, setItem: () => {} }} />);
  expect(screen.getByLabelText("Time zone")).toHaveValue("UTC");
  const plan = within(screen.getByRole("article", { name: "Plan A" }));
  expect(plan.getByText("2020-01-01 21-30")).toBeInTheDocument();
  expect(plan.getByText("2020-01-01 22-00")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: "Asia/Shanghai" } });
  expect(plan.getByText("2020-01-02 05-30")).toBeInTheDocument();
  expect(plan.getByText("2020-01-02 06-00")).toBeInTheDocument();
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
  expect(plan.getByText("2024-03-10 01-30")).toBeInTheDocument();
  expect(plan.getByText("2024-03-10 03-30")).toBeInTheDocument();
  expect(plan.getByText("Inferred arrival")).toBeInTheDocument();
  expect(plan.getByText("Arrival not supplied; inferred time is display arithmetic only")).toBeInTheDocument();
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
  expect(plan.getByText("2024-03-10 09-15")).toBeInTheDocument();
  expect(plan.getByText("10-20")).toBeInTheDocument();
  expect(plan.getAllByText("Time zone not supplied; not converted")).toHaveLength(2);
  expect(plan.getAllByText("Time unavailable for conversion; original value retained")).toHaveLength(2);
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
  expect(plan.getByText("2024-01-02 00-00")).toBeInTheDocument();
  const india = screen.getByRole("option", { name: /^Asia\/(Kolkata|Calcutta)$/ }) as HTMLOptionElement;
  fireEvent.change(screen.getByLabelText("Time zone"), { target: { value: india.value } });
  expect(plan.getByText("2024-01-02 05-30")).toBeInTheDocument();
  expect(plan.getByText("2024-01-02 06-00")).toBeInTheDocument();
});
