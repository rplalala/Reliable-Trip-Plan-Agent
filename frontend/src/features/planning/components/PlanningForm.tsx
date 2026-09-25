import { useEffect, useState } from "react";

import {
  latestEndDate,
  addCalendarDays,
  type TripDateWindow,
  isDateWithinTripWindow,
} from "../datePolicy";
import { getTripDateWindow } from "../api";
import type { ProductPlanningInput } from "../types";

interface PlanningFormProps {
  isSubmitting: boolean;
  onSubmit: (input: ProductPlanningInput) => void;
  onEdit?: () => void;
}

export function PlanningForm({ isSubmitting, onSubmit, onEdit }: PlanningFormProps) {
  const [dateWindow, setDateWindow] = useState<TripDateWindow | null>(null);
  const [dateError, setDateError] = useState(false);
  useEffect(() => {
    let active = true;
    getTripDateWindow().then(
      (window) => { if (active) setDateWindow(window); },
      () => { if (active) setDateError(true); },
    );
    return () => { active = false; };
  }, []);
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travelerCount, setTravelerCount] = useState("");
  const [budgetAmount, setBudgetAmount] = useState("");
  const [budgetCurrency, setBudgetCurrency] = useState("");
  const [additionalPreferences, setAdditionalPreferences] = useState("");

  const parsedTravelerCount = Number(travelerCount);
  const hasRequiredFields =
    destination.trim().length > 0 &&
    startDate.length > 0 &&
    endDate.length > 0 &&
    Number.isInteger(parsedTravelerCount) &&
    parsedTravelerCount >= 1;
  const hasValidDateRange = !startDate || !endDate || endDate >= startDate;
  const hasValidDateWindow = dateWindow !== null &&
    (!startDate || isDateWithinTripWindow(startDate, dateWindow)) &&
    (!endDate || isDateWithinTripWindow(endDate, dateWindow));
  const hasBudgetAmount = budgetAmount.trim().length > 0;
  const hasBudgetCurrency = budgetCurrency.trim().length > 0;
  const hasBudget = hasBudgetAmount || hasBudgetCurrency;
  const hasValidBudget =
    !hasBudget ||
    (hasBudgetAmount &&
      hasBudgetCurrency &&
      Number.isFinite(Number(budgetAmount)) &&
      Number(budgetAmount) >= 0 &&
      /^[A-Z]{3}$/.test(budgetCurrency));
  const hasValidDuration = !startDate || !endDate || !dateWindow || endDate <= addCalendarDays(startDate, dateWindow.maxTripDays - 1);
  const canSubmit =
    hasRequiredFields &&
    hasValidDuration &&
    hasValidDateRange &&
    hasValidDateWindow &&
    hasValidBudget &&
    !isSubmitting;

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) {
      return;
    }

    const input: ProductPlanningInput = {
      destination,
      start_date: startDate,
      end_date: endDate,
      traveler_count: parsedTravelerCount,
    };
    if (hasBudgetAmount && hasBudgetCurrency) {
      input.budget = {
        amount: budgetAmount,
        currency: budgetCurrency,
      };
    }
    if (additionalPreferences.trim().length > 0) {
      input.additional_preferences = additionalPreferences;
    }
    onSubmit(input);
  }

  return (
    <form className="planning-form" onSubmit={handleSubmit} onChange={onEdit}>
      <div className="product-form-grid">
        <label className="field-wide">
          Destination
          <input
            type="text"
            value={destination}
            required
            disabled={isSubmitting}
            placeholder="Beijing"
            onChange={(event) => setDestination(event.target.value)}
          />
        </label>
        <label>
          Start date
          <input
            type="date"
            value={startDate}
            min={dateWindow?.allowedStart}
            max={dateWindow?.allowedEnd}
            required
            disabled={isSubmitting}
            aria-describedby={!hasValidDateWindow ? "date-window-error" : undefined}
            onChange={(event) => setStartDate(event.target.value)}
          />
        </label>
        <label>
          End date
          <input
            type="date"
            value={endDate}
            min={startDate || dateWindow?.allowedStart}
            max={dateWindow ? latestEndDate(startDate, dateWindow) : undefined}
            required
            disabled={isSubmitting}
            aria-describedby={
              !hasValidDateWindow
                ? "date-window-error"
                : !hasValidDateRange
                  ? "date-range-error"
                  : undefined
            }
            onChange={(event) => setEndDate(event.target.value)}
          />
        </label>
        {!dateWindow && <p>{dateError ? "Date limits could not be loaded. Reload to try again." : "Loading date limits…"}</p>}
        {!hasValidDuration && <p className="field-error">Trips may last at most 10 days, including both dates.</p>}
        {dateWindow && !hasValidDateWindow && (
          <p className="field-error field-wide" id="date-window-error">
            Travel dates must be between {dateWindow?.allowedStart} and {dateWindow?.allowedEnd}.
          </p>
        )}
        {!hasValidDateRange && (
          <p className="field-error field-wide" id="date-range-error">
            End date must be on or after the start date.
          </p>
        )}
        <label>
          Travelers
          <input
            type="number"
            value={travelerCount}
            min="1"
            step="1"
            required
            disabled={isSubmitting}
            placeholder="2"
            onChange={(event) => setTravelerCount(event.target.value)}
          />
        </label>
      </div>

      <fieldset className="budget-fields">
        <legend>Budget <span>Optional</span></legend>
        <p className="field-help">If you add a budget, provide both the amount and currency.</p>
        <div className="product-form-grid">
          <label>
            Budget amount
            <input
              type="number"
              value={budgetAmount}
              min="0"
              step="0.01"
              disabled={isSubmitting}
              placeholder="2000"
              aria-describedby={!hasValidBudget ? "budget-error" : undefined}
              onChange={(event) => setBudgetAmount(event.target.value)}
            />
          </label>
          <label>
            Currency
            <input
              type="text"
              value={budgetCurrency}
              pattern="[A-Z]{3}"
              maxLength={3}
              disabled={isSubmitting}
              placeholder="AUD"
              aria-describedby={!hasValidBudget ? "budget-error" : undefined}
              onChange={(event) => setBudgetCurrency(event.target.value)}
            />
          </label>
          {!hasValidBudget && (
            <p className="field-error field-wide" id="budget-error">
              Enter a non-negative amount and a three-letter uppercase currency code.
            </p>
          )}
        </div>
      </fieldset>

      <label htmlFor="additional-preferences">
        Additional preferences <span className="optional-label">Optional</span>
      </label>
      <p className="field-help" id="additional-preferences-help">
        Add interests, preferred pace, accessibility needs, or anything else you want considered.
      </p>
      <textarea
        id="additional-preferences"
        aria-describedby="additional-preferences-help"
        value={additionalPreferences}
        onChange={(event) => setAdditionalPreferences(event.target.value)}
        placeholder="I enjoy local food, museums, and quiet mornings."
        rows={5}
        disabled={isSubmitting}
      />
      <div className="form-actions">
        <button
          className="button button-primary"
          type="submit"
          disabled={!canSubmit}
        >
          {isSubmitting ? "Building your itinerary…" : "Generate itinerary"}
        </button>
        <span className="form-note">Generation may take a moment.</span>
      </div>
    </form>
  );
}
