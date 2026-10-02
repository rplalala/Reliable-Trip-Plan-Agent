import { expect, it } from "vitest";
import { importAnswers, latestAnswer } from "./answers";
import type { Answer, Presentation } from "./answers";

const presentation = { batch_id: "b", batch_revision: 1, presentation_id: "p", presentation_hash: "hash", rater_ref: "r",
  tasks: [{ task_id: "task-1" }] } as Presentation;
function answer(revision = 1): Answer {
  return { answer_schema_version: "rtpeval_human_answer_1", batch_id: "b", batch_revision: 1, presentation_id: "p", presentation_hash: "hash", rater_ref: "r", task_id: "task-1",
    answer_revision: revision, updated_at: "2026-10-02T00:00:00Z", state: "submitted",
    responses: { preference: { status: "ranked", tie_groups: [["A", "C"], ["B"], ["D"]] }, pace: { status: "unable_to_judge" }, usefulness: { status: "not_applicable" } } };
}
const bundle = (...answers: Answer[]) => ({ schema_version: "rtpeval_human_answers_1", answers });
it("same revision replay is idempotent and conflicts cannot overwrite answers", () => {
  const original = answer();
  const retained = importAnswers(bundle(original), presentation);
  expect(importAnswers(bundle(original), presentation, retained)).toHaveLength(1);
  expect(() => importAnswers(bundle({ ...original, updated_at: "2026-10-02T01:00:00Z" }), presentation, retained)).toThrow("Conflicting revision");
  expect(retained).toEqual([original]);
});
it("revision order controls effective submission and draft retains incomplete ranking", () => {
  const draft: Answer = { ...answer(3), state: "draft", responses: { preference: { status: "ranked", tie_groups: [["A"]] } } };
  const imported = importAnswers(bundle(answer(2), draft, answer()), presentation);
  expect(latestAnswer(imported, "task-1", true)?.answer_revision).toBe(2);
  expect(latestAnswer(imported, "task-1")?.state).toBe("draft");
  expect(() => importAnswers(bundle({ ...draft, state: "submitted" }), presentation)).toThrow();
});
it("stale presentation, duplicate labels and private fields are rejected", () => {
  expect(() => importAnswers(bundle({ ...answer(), presentation_hash: "stale" }), presentation)).toThrow("Stale");
  const invalid = answer(); invalid.responses.preference = { status: "ranked", tie_groups: [["A", "A", "B", "D"]] };
  expect(() => importAnswers(bundle(invalid), presentation)).toThrow("each label");
  expect(() => importAnswers(bundle({ ...answer(), mapping: {} } as Answer), presentation)).toThrow("Unexpected answer fields");
});
