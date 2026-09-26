import { useEffect, useRef, useState } from "react";
import { submitDeveloperPlanningRequest } from "../../features/developer-planning/api";
import { RawJsonView } from "../../features/developer-planning/components/RawJsonView";
import type { DeveloperVersion } from "../../features/developer-planning/types";
import { getTripDateWindow } from "../../features/planning/api";
import { PlanningForm } from "../../features/planning/components/PlanningForm";
import { TripDateInput } from "../../features/planning/components/TripDateInput";
import { isValidISODate } from "../../features/planning/datePolicy";
import { ItineraryView } from "../../features/planning/components/ItineraryView";
import type { Itinerary, ProductPlanningInput } from "../../features/planning/types";
import { HttpError } from "../../shared/api/http";
import type { PlanningEvent } from "../../shared/api/planningStream";
import { PlanningProgressBar } from "../../shared/PlanningProgressBar";
import { advanceProgress } from "../../shared/planningProgress";

const versions: DeveloperVersion[] = ["v0", "v1", "v2", "v3"];
interface Run {
  status: "idle" | "running" | "completed" | "failed" | "cancelled";
  events: PlanningEvent[];
  dropped: number;
  position: number;
  response?: unknown;
}
const idleRun = (): Run => ({ status: "idle", events: [], dropped: 0, position: 0 });
const initialRuns = (): Record<DeveloperVersion, Run> => ({ v0: idleRun(), v1: idleRun(), v2: idleRun(), v3: idleRun() });
interface Snapshot { request: ProductPlanningInput; reference_date: string }

function resultItinerary(value: unknown): Itinerary | null {
  if (!value || typeof value !== "object" || !("itinerary" in value)) return null;
  const itinerary = value.itinerary as Itinerary;
  return itinerary && Array.isArray(itinerary.days) && typeof itinerary.destination === "string" ? itinerary : null;
}

export function DeveloperPlannerPage() {
  const [referenceDate, setReferenceDate] = useState("");
  const [dateError, setDateError] = useState(false);
  const [runs, setRuns] = useState(initialRuns);
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const controllers = useRef(new Map<DeveloperVersion, AbortController>());
  const group = useRef(0);
  const busy = versions.some(v => runs[v].status === "running");
  useEffect(() => {
    let mounted = true;
    const owned = controllers.current;
    getTripDateWindow().then(
      window => { if (mounted) setReferenceDate(value => value || window.allowedStart); },
      () => { if (mounted) setDateError(true); },
    );
    return () => { mounted = false; owned.forEach(c => c.abort()); owned.clear(); };
  }, []);

  function start(version: DeveloperVersion, input: Snapshot, generation: number) {
    if (controllers.current.has(version)) return;
    const controller = new AbortController();
    controllers.current.set(version, controller);
    const current = () => group.current === generation && controllers.current.get(version) === controller && !controller.signal.aborted;
    setRuns(previous => ({ ...previous, [version]: { ...idleRun(), status: "running" } }));
    void submitDeveloperPlanningRequest({ version, ...input }, {
      signal: controller.signal,
      onEvent: event => {
        if (!current()) return;
        setRuns(previous => {
          const run = previous[version];
          const events = [...run.events, event];
          const excess = Math.max(0, events.length - 500);
          return { ...previous, [version]: { ...run, position: advanceProgress(run.position, event, version), events: events.slice(-500), dropped: run.dropped + (event.dropped_events || 0) + excess } };
        });
      },
    }).then(response => {
      if (current()) setRuns(previous => ({ ...previous, [version]: { ...previous[version], status: "completed", position: 1, response } }));
    }).catch(error => {
      if (!current()) return;
      if (error instanceof DOMException && error.name === "AbortError") {
        setRuns(previous => ({ ...previous, [version]: { ...previous[version], status: "cancelled" } }));
      } else {
        setRuns(previous => ({ ...previous, [version]: { ...previous[version], status: "failed", response: error instanceof HttpError ? { http_status: error.status, response: error.body } : { error: "developer_request_failed" } } }));
      }
    }).finally(() => {
      if (controllers.current.get(version) === controller) controllers.current.delete(version);
    });
  }

  function stop(version: DeveloperVersion) {
    controllers.current.get(version)?.abort();
    controllers.current.delete(version);
    setRuns(previous => ({ ...previous, [version]: { ...previous[version], status: "cancelled", response: undefined } }));
  }

  function editInput() {
    if (controllers.current.size) return;
    group.current++; setSnapshot(null); setRuns(initialRuns());
  }

  return <div>
    <h2>Run all research planners</h2>
    <p>One input, four independent runs. Results are not automatically ranked. Reloading loses this session.</p>
    <TripDateInput label="Reference date" value={referenceDate} disabled={busy}
      onChange={value => { setReferenceDate(value); editInput(); }} />
    {dateError && <p role="alert">Date limits could not be loaded. Reload to try again.</p>}
    <PlanningForm isSubmitting={busy || !isValidISODate(referenceDate)} referenceDate={isValidISODate(referenceDate) ? referenceDate : undefined} submitLabel="Run all versions"
      onEdit={editInput} onSubmit={request => {
        if (controllers.current.size || !referenceDate) return;
        const input = structuredClone({ request, reference_date: referenceDate });
        group.current++; setSnapshot(input); setRuns(initialRuns());
        versions.forEach(v => start(v, input, group.current));
      }} />
    {busy && <button className="button button-stop" type="button" onClick={() => versions.forEach(v => { if (controllers.current.has(v)) stop(v); })}>Stop all</button>}
    {snapshot && <details><summary>Run group input snapshot</summary><pre>{JSON.stringify(snapshot, null, 2)}</pre></details>}
    <div className="research-runs">{versions.map(version => {
      const run = runs[version];
      const itinerary = resultItinerary(run.response);
      const latest = run.events.at(-1);
      const latestStage = run.events.filter(e => e.type === "stage").at(-1);
      return <section className="research-run" aria-label={`${version.toUpperCase()} run`} key={version}>
        <h3>{version.toUpperCase()}</h3><p role="status">{run.status}</p>
        <PlanningProgressBar label={`${version.toUpperCase()} progress`} value={run.position} state={run.status} message={run.status === "running" ? latestStage?.message : run.status} />
        {latest && <p>Elapsed: {(latest.elapsed_ms / 1000).toFixed(1)} s</p>}
        {latestStage && <p>{latestStage.message || latestStage.stage}</p>}
        {run.status === "running" && <button className="button button-stop" onClick={() => stop(version)}>Stop {version.toUpperCase()}</button>}
        {run.status !== "running" && snapshot && <button className="button button-secondary" onClick={() => start(version, snapshot, group.current)}>Rerun {version.toUpperCase()}</button>}
        {run.dropped > 0 && <p role="note">{run.dropped} earlier events were omitted; the event history is incomplete.</p>}
        <details><summary>Mechanism progress and timings</summary>
          <ol>{run.events.filter(e => e.type === "stage" || e.type === "detail").map(event => <li key={`${event.run_id}:${event.sequence}`}>
            <p>{event.stage || event.name} {event.occurrence ? `#${event.occurrence}` : ""}: {event.status || "details"}
              {event.duration_ms !== undefined && ` · ${(event.duration_ms / 1000).toFixed(2)} s`}</p>
            {event.parent_id && <small>Parent: {event.parent_id}</small>}
            {event.type === "detail" && event.stage_id && <small>Stage: {event.stage_id}</small>}
            {event.details !== undefined && <pre>{JSON.stringify(event.details, null, 2)}</pre>}
          </li>)}</ol>
        </details>
        {itinerary && <ItineraryView itinerary={itinerary} />}
        {run.response !== undefined && <details><summary>Complete result / debug JSON</summary><RawJsonView value={run.response} /></details>}
      </section>;
    })}</div>
  </div>;
}
