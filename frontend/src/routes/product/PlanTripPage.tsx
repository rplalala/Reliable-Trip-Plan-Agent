import { useEffect, useRef, useState } from "react";
import { PlanningProgressBar } from "../../shared/PlanningProgressBar";
import { advanceProgress } from "../../shared/planningProgress";

import { submitPlanningRequest } from "../../features/planning/api";
import { ItineraryView } from "../../features/planning/components/ItineraryView";
import { PlanningForm } from "../../features/planning/components/PlanningForm";
import type {
  ProductPlanningInput,
  ProductPlanningResponse,
} from "../../features/planning/types";

export function PlanTripPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<ProductPlanningResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState("");
  const [position, setPosition] = useState(0);
  const [progressState, setProgressState] = useState("idle");
  const active = useRef<AbortController | null>(null);
  useEffect(() => () => { active.current?.abort(); active.current = null; }, []);

  async function handleSubmit(input: ProductPlanningInput) {
    if (active.current) {
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setResult(null);
    setProgress("Starting your trip plan");
    setPosition(0);
    setProgressState("running");
    const controller = new AbortController();
    active.current = controller;
    try {
      const response = await submitPlanningRequest(input, {
        signal: controller.signal,
        onEvent: event => {
          if (active.current === controller && !controller.signal.aborted) {
            setPosition(previous => advanceProgress(previous, event, "product"));
          }
          if (active.current === controller && !controller.signal.aborted && event.type === "stage" && event.status !== "skipped" && event.message) {
            setProgress(event.message);
          }
        },
      });
      if (active.current === controller && !controller.signal.aborted) {
        setResult(response);
        setProgressState(response.status === "completed" ? "completed" : "paused");
        setProgress(response.status === "completed"
          ? response.policy_completion === "incomplete"
            ? "Planning finished with unmet requirements. Review the itinerary below."
            : "Your itinerary is ready"
          : "Planning paused. Please review the message below.");
        if (response.status === "completed") setPosition(1);
      }
    } catch {
      if (active.current === controller && !controller.signal.aborted) {
        setError("We could not generate your itinerary. Please try again.");
        setProgressState("failed");
        setProgress("Planning could not be completed");
      }
    } finally {
      if (active.current === controller) {
        active.current = null;
        setIsSubmitting(false);
      }
    }
  }

  return (
    <div className="planner-page page-width">
      <header className="page-heading">
        <p className="eyebrow">Plan a trip</p>
        <h1>What would make this trip feel right?</h1>
        <p>Start with the essentials. Add as much context as you like.</p>
      </header>

      <PlanningForm
        isSubmitting={isSubmitting}
        onSubmit={handleSubmit}
        onEdit={() => { setResult(null); setError(null); setProgressState("idle"); setPosition(0); }}
      />

      {progressState !== "idle" && <section aria-label="Planning progress" className="planning-progress-panel">
        <p role="status">{progress}</p>
        <PlanningProgressBar label="Planning progress" value={position} state={progressState} message={progress} />
        {isSubmitting && <button className="button button-stop" type="button" onClick={() => {
          active.current?.abort(); active.current = null;
          setIsSubmitting(false); setProgress("Planning stopped"); setProgressState("cancelled");
          setError("Planning stopped. You can edit your trip and try again.");
        }}>Stop planning</button>}
      </section>}

      <div aria-live="polite">
        {error && <div className="alert alert-error">{error}</div>}
        {result?.status === "needs_clarification" && (
          <section className="alert alert-clarification">
            <h2>{result.issues?.input_disposition === "REWRITE_REQUIRED"
              ? "Please revise the conflicting trip details"
              : "We couldn't interpret some of your trip details"}</h2>
            <p>Please review them and try again.</p>
            {result.issues?.issues?.map((issue, index) => (
              <div key={index}>
                {issue.source_refs.map((source, sourceIndex) => (
                  <blockquote key={sourceIndex}>{source.quote}</blockquote>
                ))}
                {issue.quote_status === "unavailable" && <p>Original quote unavailable.</p>}
                {issue.related_field && (
                  <p>Current {issue.related_field}: {String(issue.current_value ?? "")}</p>
                )}
                <p>{issue.reason}</p>
                <p>{issue.action}</p>
              </div>
            ))}
          </section>
        )}
        {result?.status === "provider_blocked" && (
          <section className="alert alert-clarification" role="status">
            <h2>Please revise your preferences</h2>
            <p>{result.message}</p>
            <p>{result.action}</p>
          </section>
        )}
        {result?.status === "safety_blocked" && (
          <section className="alert" role="status">
            <h2>Travel planning paused</h2>
            <p>{result.message}</p>
            <p>{result.action}</p>
          </section>
        )}
      </div>

      {result?.status === "completed" && <ItineraryView itinerary={result.itinerary} minimumCoverage={result.minimum_daily_coverage} policyCompletion={result.policy_completion} />}
    </div>
  );
}
