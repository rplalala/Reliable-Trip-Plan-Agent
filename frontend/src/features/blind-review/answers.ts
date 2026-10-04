export const labels = ["A", "B", "C", "D"] as const;
export const dimensions = ["preference", "pace", "usefulness"] as const;
export type Dimension = typeof dimensions[number];
export type Response = { status: "ranked"; tie_groups: string[][]; reason?: string } |
  { status: "pending" | "unable_to_judge" | "not_applicable"; reason?: string };
export interface Presentation {
  schema_version: "rtpeval_human_package_1";
  batch_id: string; batch_revision: number; presentation_id: string;
  presentation_hash: string; rater_ref: string; dimensions: Dimension[];
  tasks: { task_id: string; input: Record<string, unknown>;
    plans: Record<string, { days: { date: string; items: { kind: string; fields: Record<string, unknown>; notices: string[] }[] }[] }> }[];
}
export interface Answer {
  answer_schema_version: "rtpeval_human_answer_1";
  batch_id: string; batch_revision: number; presentation_id: string;
  presentation_hash: string; rater_ref: string; task_id: string;
  answer_revision: number; updated_at: string; state: "draft" | "submitted";
  responses: Partial<Record<Dimension, Response>>;
}
export interface Bundle { schema_version: "rtpeval_human_answers_1"; answers: Answer[] }
const identity = ["batch_id", "batch_revision", "presentation_id", "presentation_hash", "rater_ref"] as const;
const answerKeys = [...identity, "answer_schema_version", "task_id", "answer_revision", "updated_at", "state", "responses"].sort();
function object(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}
function check(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}
function stable(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stable).join(",")}]`;
  if (object(value)) return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${stable(value[k])}`).join(",")}}`;
  return JSON.stringify(value);
}
export function complete(responses: Partial<Record<Dimension, Response>>): boolean {
  return dimensions.every(d => {
    const r = responses[d];
    return r && (r.status === "unable_to_judge" || r.status === "not_applicable" ||
      (r.status === "ranked" && r.tie_groups.flat().length === 4 && new Set(r.tie_groups.flat()).size === 4));
  });
}
export function importAnswers(value: unknown, presentation: Presentation, previous: Answer[] = []): Answer[] {
  check(object(value) && Object.keys(value).sort().join() === "answers,schema_version" &&
    value.schema_version === "rtpeval_human_answers_1" && Array.isArray(value.answers), "Invalid answer bundle");
  const combined = [...previous, ...value.answers];
  const retained = new Map<string, Answer>();
  for (const raw of combined) {
    check(object(raw) && Object.keys(raw).sort().join() === answerKeys.join(), "Unexpected answer fields");
    check(raw.answer_schema_version === "rtpeval_human_answer_1" && identity.every(k => raw[k] === presentation[k]), "Stale presentation or rater");
    check(presentation.tasks.some(t => t.task_id === raw.task_id), "Unknown task");
    check(typeof raw.answer_revision === "number" && Number.isSafeInteger(raw.answer_revision) && raw.answer_revision > 0, "Invalid revision");
    check(typeof raw.updated_at === "string" && /(?:Z|[+-]\d\d:\d\d)$/.test(raw.updated_at) && !Number.isNaN(Date.parse(raw.updated_at)), "Invalid timestamp");
    check(raw.state === "draft" || raw.state === "submitted", "Invalid answer state");
    check(object(raw.responses) && Object.keys(raw.responses).every(k => dimensions.includes(k as Dimension)), "Invalid dimensions");
    for (const r of Object.values(raw.responses)) {
      check(object(r) && Object.keys(r).every(k => ["status", "reason", "tie_groups"].includes(k)) &&
        (r.reason === undefined || typeof r.reason === "string"), "Invalid response");
      check(["ranked", "unable_to_judge", "not_applicable", "pending"].includes(String(r.status)) &&
        (r.status !== "pending" || raw.state === "draft"), "Invalid response state");
      if (r.status === "ranked") {
        check(Array.isArray(r.tie_groups) && r.tie_groups.every(g => Array.isArray(g) && g.length > 0), "Invalid tie groups");
        const ranked = r.tie_groups.flat();
        check(ranked.every(l => labels.includes(l)) && new Set(ranked).size === ranked.length &&
          (raw.state === "draft" || ranked.length === 4), "Ranking must include each label exactly once");
      } else check(!("tie_groups" in r), "Unassessable response cannot rank labels");
    }
    const record = raw as unknown as Answer;
    check(record.state === "draft" || complete(record.responses), "Incomplete submitted answer");
    const key = `${record.task_id}:${record.answer_revision}`;
    check(!retained.has(key) || stable(retained.get(key)) === stable(record), "Conflicting revision; no answers imported");
    retained.set(key, record);
  }
  return [...retained.values()].sort((a, b) => a.task_id.localeCompare(b.task_id) || a.answer_revision - b.answer_revision);
}
export function latestAnswer(answers: Answer[], task: string, submittedOnly = false): Answer | undefined {
  return answers.filter(a => a.task_id === task && (!submittedOnly || a.state === "submitted"))
    .sort((a, b) => b.answer_revision - a.answer_revision)[0];
}
