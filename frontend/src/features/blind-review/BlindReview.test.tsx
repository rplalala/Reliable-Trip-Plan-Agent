import { fireEvent, render, screen } from "@testing-library/react";
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
  fireEvent.change(screen.getByLabelText("pace: response"), { target: { value: "unable_to_judge" } });
  fireEvent.click(screen.getByRole("button", { name: "Submit answer" }));
  expect(screen.getByText("Submitted revision 2")).toBeInTheDocument();
  const saved = JSON.parse([...storage.values()][0]);
  expect(saved.answers).toHaveLength(2);
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
  expect(screen.getByText("2020-01-01T10:30:00+00:00")).toBeInTheDocument();
});
