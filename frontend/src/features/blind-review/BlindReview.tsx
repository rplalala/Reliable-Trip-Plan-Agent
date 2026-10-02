import { useState } from "react";
import { complete, dimensions, importAnswers, labels, latestAnswer } from "./answers";
import type { Answer, Bundle, Dimension, Presentation, Response } from "./answers";
import { DisplayTime, TimeZonePicker } from "./DisplayTime";
import "./review.css";

type Storage = Pick<globalThis.Storage, "getItem" | "setItem">;
type Draft = Record<Dimension, { status: Response["status"]; ranks: Record<string, string>; reason: string }>;
function draft(answer?: Answer): Draft {
  return Object.fromEntries(dimensions.map(d => {
    const r = answer?.responses[d];
    return [d, { status: r?.status ?? "ranked", reason: r?.reason ?? "", ranks: Object.fromEntries(labels.map(label =>
      [label, r?.status === "ranked" ? String(r.tie_groups.findIndex(g => g.includes(label)) + 1 || "") : ""])) }];
  })) as Draft;
}
function responses(form: Draft): Record<Dimension, Response> {
  return Object.fromEntries(dimensions.map(d => {
    const f = form[d];
    const ranked = ["1", "2", "3", "4"].map(position => labels.filter(l => f.ranks[l] === position)).filter(g => g.length);
    return [d, { status: f.status, ...(f.status === "ranked" ? { tie_groups: ranked } : {}),
      ...(f.reason ? { reason: f.reason } : {}) }];
  })) as Record<Dimension, Response>;
}
function display(value: unknown): string {
  if (value === null || value === undefined) return "Not supplied";
  if (Array.isArray(value)) return value.map(display).join("; ");
  if (typeof value === "object") return Object.entries(value).map(([k, v]) => `${k}: ${display(v)}`).join("; ");
  return String(value);
}
const names: Record<string, string> = {
  additional_preferences: "Original preferences", start_date: "Start date", end_date: "End date",
  traveler_count: "Travelers", estimated_cost: "Displayed cost", place_name: "Place", start_time: "Start",
  end_time: "End", departure_time: "Departure", arrival_time: "Supplied arrival", inferred_arrival: "Inferred arrival",
  duration_seconds: "Travel duration (seconds)", distance_meters: "Distance (meters)",
  reserve_seconds: "Reserve (seconds)", calculation_basis: "Duration basis",
};
const timeFields = new Set(["start_time", "end_time", "departure_time", "arrival_time", "inferred_arrival"]);
function Fields({ fields, zone }: { fields: Record<string, unknown>; zone: string }) {
  return <dl>{Object.entries(fields).filter(([key]) => key !== "unknowns").map(([key, value]) => <div key={key}><dt>{names[key] ?? key.replaceAll("_", " ")}</dt>
    <dd>{timeFields.has(key) ? <DisplayTime value={value} zone={zone} /> : display(value)}</dd></div>)}</dl>;
}
function download(bundle: Bundle) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(bundle, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url; link.download = "answers.json"; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function BlindReview({ presentation, storage }: { presentation: Presentation; storage?: Storage }) {
  const [zone, setZone] = useState("UTC");
  const key = `blind-review:${presentation.presentation_id}:${presentation.presentation_hash}:${presentation.rater_ref}`;
  const [initial] = useState(() => {
    try {
      const raw = (storage ?? window.localStorage).getItem(key);
      return { answers: raw ? importAnswers(JSON.parse(raw), presentation) : [], error: "" };
    } catch { return { answers: [], error: "Local restore unavailable. Import your downloaded JSON backup." }; }
  });
  const [answers, setAnswers] = useState<Answer[]>(initial.answers);
  const [index, setIndex] = useState(0);
  const task = presentation.tasks[index];
  const [form, setForm] = useState(() => draft(latestAnswer(initial.answers, task.task_id)));
  const [error, setError] = useState(initial.error);
  const [notice, setNotice] = useState("");
  const [clearRequested, setClearRequested] = useState(false);
  const submitted = latestAnswer(answers, task.task_id, true);
  const currentResponses = responses(form);
  function persist(next: Answer[]) {
    setAnswers(next);
    try {
      (storage ?? window.localStorage).setItem(key, JSON.stringify({ schema_version: "rtpeval_human_answers_1", answers: next }));
      setError(""); setNotice("Saved locally. Download JSON for a portable backup.");
    } catch { setError("Local save failed. Answers remain in this window; download JSON before closing."); setNotice(""); }
  }
  function save(state: Answer["state"]) {
    const record: Answer = {
      answer_schema_version: "rtpeval_human_answer_1", batch_id: presentation.batch_id, batch_revision: presentation.batch_revision,
      presentation_id: presentation.presentation_id, presentation_hash: presentation.presentation_hash, rater_ref: presentation.rater_ref,
      task_id: task.task_id, answer_revision: (latestAnswer(answers, task.task_id)?.answer_revision ?? 0) + 1,
      updated_at: new Date().toISOString(), state, responses: currentResponses,
    };
    persist(importAnswers({ schema_version: "rtpeval_human_answers_1", answers: [record] }, presentation, answers));
  }
  function navigate(next: number) {
    setIndex(next); setForm(draft(latestAnswer(answers, presentation.tasks[next].task_id))); setNotice("");
  }
  function clearAnswers() {
    try {
      (storage ?? window.localStorage).setItem(key, JSON.stringify({ schema_version: "rtpeval_human_answers_1", answers: [] }));
    } catch {
      setError("Local clear failed. Answers are unchanged; download JSON before closing."); setNotice(""); return;
    }
    setAnswers([]); setIndex(0); setForm(draft()); setClearRequested(false); setError("");
    setNotice("Answers cleared for this review package.");
  }
  async function read(file?: File) {
    if (!file) return;
    try {
      const text = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader(); reader.onload = () => resolve(String(reader.result));
        reader.onerror = () => reject(new Error("File read failed")); reader.readAsText(file);
      });
      const imported = importAnswers(JSON.parse(text), presentation, answers);
      persist(imported); setForm(draft(latestAnswer(imported, task.task_id)));
    } catch (e) { setError(`Import rejected: ${e instanceof Error ? e.message : "Invalid file"}`); }
  }
  return <main className="blind-review">
    <header><h1>Travel plan review</h1><p>Compare the four plans against the original request. Position 1 is best; assign the same position for a tie.</p>
      <p>Use Unable to judge for insufficient information and Not applicable when a dimension does not apply. Save drafts before changing tasks; download JSON before closing.</p>
      <TimeZonePicker value={zone} onChange={setZone} /><p>Times with supplied offsets are shown in {zone} using a 24-hour HH:mm clock and the converted date.
        Source day headings retain the original grouping.</p></header>
    <nav aria-label="Task navigation"><button disabled={index === 0} onClick={() => navigate(index - 1)}>Previous task</button>
      <strong>Task {index + 1} of {presentation.tasks.length}</strong><button disabled={index === presentation.tasks.length - 1} onClick={() => navigate(index + 1)}>Next task</button></nav>
    <section aria-label="Original request"><h2>Original request</h2><Fields fields={task.input} zone={zone} /></section>
    <div className="plans">{labels.map(label => <article key={label} aria-label={`Plan ${label}`}><h2>Plan {label}</h2>
      {task.plans[label].days.map((day, i) => <section key={i}><h3>Source day: {day.date}</h3>{day.items.map((item, n) => <div className="item" key={n}>
        <strong>{item.kind === "travel" ? "Travel" : "Activity"}</strong><Fields fields={item.fields} zone={zone} />
      </div>)}</section>)}</article>)}</div>
    <section aria-label="Your rankings"><h2>Your rankings</h2>{dimensions.map(d => <fieldset key={d}><legend>{d === "preference" ? "Preference match" : d === "pace" ? "Pace" : "Practical usefulness"}</legend>
      <label>Response <select aria-label={`${d}: response`} value={form[d].status} onChange={e => setForm({ ...form, [d]: { ...form[d], status: e.target.value as Response["status"] } })}>
        <option value="ranked">Rank plans</option><option value="unable_to_judge">Unable to judge</option><option value="not_applicable">Not applicable</option></select></label>
      <div className="ranks">{labels.map(label => <label key={label}>Plan {label}<select aria-label={`${d}: position for ${label}`} disabled={form[d].status !== "ranked"} value={form[d].ranks[label]}
        onChange={e => setForm({ ...form, [d]: { ...form[d], ranks: { ...form[d].ranks, [label]: e.target.value } } })}>
        <option value="">Choose position</option>{[1, 2, 3, 4].map(n => <option key={n} value={n}>{n}</option>)}</select></label>)}</div>
      <label>Reason (optional)<textarea aria-label={`${d}: reason`} value={form[d].reason} onChange={e => setForm({ ...form, [d]: { ...form[d], reason: e.target.value } })} /></label>
    </fieldset>)}</section>
    {submitted && <p>Submitted revision {submitted.answer_revision}</p>}
    {error && <p role="alert">{error}</p>}{notice && <p role="status">{notice}</p>}
    <footer><button onClick={() => save("draft")}>Save draft</button><button disabled={!complete(currentResponses)} onClick={() => save("submitted")}>Submit answer</button>
      <button onClick={() => download({ schema_version: "rtpeval_human_answers_1", answers })}>Download answers JSON</button>
      <label>Import answers JSON<input type="file" accept="application/json,.json" onChange={e => { void read(e.target.files?.[0]); e.target.value = ""; }} /></label>
      <button onClick={() => setClearRequested(true)}>Clear answers</button></footer>
    {clearRequested && <section aria-label="Clear answers confirmation">
      <p>This clears all answers, drafts and revisions for this review package in this browser. Download a JSON backup first.
        Downloaded files and other review packages are unchanged.</p>
      <button onClick={() => setClearRequested(false)}>Cancel clear</button>{" "}<button onClick={clearAnswers}>Confirm clear</button>
    </section>}
  </main>;
}
