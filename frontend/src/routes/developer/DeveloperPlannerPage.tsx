import { useState } from "react";

import { submitDeveloperPlanningRequest } from "../../features/developer-planning/api";
import { DeveloperPlanningForm } from "../../features/developer-planning/components/DeveloperPlanningForm";
import { RawJsonView } from "../../features/developer-planning/components/RawJsonView";
import type { DeveloperVersion } from "../../features/developer-planning/types";
import { getBrowserLocalDate } from "../../features/planning/datePolicy";
import { HttpError } from "../../shared/api/http";

const IMPLEMENTED_VERSION: DeveloperVersion = "v0";

export function DeveloperPlannerPage() {
  const [requestText, setRequestText] = useState("");
  const [referenceDate, setReferenceDate] = useState(() => getBrowserLocalDate());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [response, setResponse] = useState<unknown>(null);

  async function handleSubmit() {
    if (!requestText.trim() || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setResponse(null);
    try {
      setResponse(
        await submitDeveloperPlanningRequest({
          version: IMPLEMENTED_VERSION,
          request_text: requestText.trim(),
          reference_date: referenceDate,
        }),
      );
    } catch (error) {
      setResponse(
        error instanceof HttpError
          ? { http_status: error.status, response: error.body }
          : { error: "developer_request_failed" },
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="developer-grid">
      <section>
        <div className="developer-section-heading">
          <p className="eyebrow">Version-aware execution</p>
          <h2>Run the current research planner</h2>
          <p>Submit one request and inspect the programmatic planner response.</p>
        </div>
        <DeveloperPlanningForm
          version={IMPLEMENTED_VERSION}
          requestText={requestText}
          referenceDate={referenceDate}
          isSubmitting={isSubmitting}
          onRequestTextChange={setRequestText}
          onReferenceDateChange={setReferenceDate}
          onSubmit={handleSubmit}
        />
      </section>
      {response === null ? (
        <section className="json-placeholder">
          <p>Raw PlanningResult or debug response will appear here.</p>
        </section>
      ) : (
        <RawJsonView value={response} />
      )}
    </div>
  );
}
