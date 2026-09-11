import { useState } from "react";

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

  async function handleSubmit(input: ProductPlanningInput) {
    if (isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setResult(null);
    try {
      setResult(await submitPlanningRequest(input));
    } catch {
      setError("We could not generate your itinerary. Please try again.");
    } finally {
      setIsSubmitting(false);
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
      />

      <div aria-live="polite">
        {error && <div className="alert alert-error">{error}</div>}
        {result?.status === "needs_clarification" && (
          <section className="alert alert-clarification">
            <h2>We couldn't interpret some of your trip details</h2>
            <p>Please review them and try again.</p>
          </section>
        )}
      </div>

      {result?.status === "completed" && <ItineraryView itinerary={result.itinerary} />}
    </div>
  );
}
