import { useEffect, useState } from "react";

import {
  latestEndDate,
  addCalendarDays,
  type TripDateWindow,
  isDateWithinTripWindow,
  isValidISODate,
} from "../datePolicy";
import { getTripDateWindow } from "../api";
import { isListedCurrency } from "../currencies";
import type { ProductPlanningInput } from "../types";
import { CurrencySelect } from "./CurrencySelect";
import { DestinationCombobox } from "./DestinationCombobox";
import { TripDateInput } from "./TripDateInput";

interface PlanningFormProps {
  isSubmitting: boolean;
  onSubmit: (input: ProductPlanningInput) => void;
  onEdit?: () => void;
  submitLabel?: string;
  referenceDate?: string;
}

export function PlanningForm({ isSubmitting, onSubmit, onEdit, submitLabel, referenceDate }: PlanningFormProps) {
  const [serverDateWindow, setDateWindow] = useState<TripDateWindow | null>(null);
  const dateWindow = referenceDate ? { allowedStart: referenceDate, allowedEnd: addCalendarDays(referenceDate, 13), maxTripDays: 10 } : serverDateWindow;
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
  const [budgetCurrency, setBudgetCurrency] = useState("AUD");
  const [additionalPreferences, setAdditionalPreferences] = useState("");

  const parsedTravelerCount = Number(travelerCount);
  const hasRequiredFields =
    destination.trim().length > 0 &&
    startDate.length > 0 &&
    endDate.length > 0 &&
    Number.isInteger(parsedTravelerCount) &&
    parsedTravelerCount >= 1;
  const hasValidDateFormat = (!startDate || isValidISODate(startDate)) &&
    (!endDate || isValidISODate(endDate));
  const hasValidDateRange = !startDate || !endDate || endDate >= startDate;
  const hasValidDateWindow = dateWindow !== null &&
    (!startDate || isDateWithinTripWindow(startDate, dateWindow)) &&
    (!endDate || isDateWithinTripWindow(endDate, dateWindow));
  const hasBudgetAmount = budgetAmount.trim().length > 0;
  const hasBudgetCurrency = budgetCurrency.trim().length > 0;
  const hasValidBudget =
    (hasBudgetAmount &&
      hasBudgetCurrency &&
      Number.isFinite(Number(budgetAmount)) &&
      Number(budgetAmount) >= 0 &&
      isListedCurrency(budgetCurrency));
  const hasValidDuration = !startDate || !endDate || !dateWindow || !isValidISODate(startDate) ||
    endDate <= addCalendarDays(startDate, dateWindow.maxTripDays - 1);
  const canSubmit =
    hasRequiredFields &&
    hasValidDateFormat &&
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
      budget: { amount: budgetAmount, currency: budgetCurrency },
    };
    if (additionalPreferences.trim().length > 0) {
      input.additional_preferences = additionalPreferences;
    }
    onSubmit(input);
  }

  return (
    <form className="planning-form" onSubmit={handleSubmit} onChange={onEdit}>
      <div className="product-form-grid">
        <DestinationCombobox value={destination} onChange={setDestination}
          onSelect={onEdit} disabled={isSubmitting} />
        <TripDateInput label="Start date" value={startDate} onChange={setStartDate} onSelect={onEdit}
          min={dateWindow?.allowedStart} max={dateWindow?.allowedEnd} disabled={isSubmitting}
          describedBy={!hasValidDateFormat ? "date-format-error" : !hasValidDateWindow ? "date-window-error" : undefined} />
        <TripDateInput label="End date" value={endDate} onChange={setEndDate} onSelect={onEdit}
          min={isValidISODate(startDate) ? startDate : dateWindow?.allowedStart}
          max={dateWindow ? latestEndDate(startDate, dateWindow) : undefined} disabled={isSubmitting}
          describedBy={!hasValidDateFormat ? "date-format-error" : !hasValidDateWindow
            ? "date-window-error" : !hasValidDateRange ? "date-range-error" : undefined} />
        {!dateWindow && <p>{dateError ? "Date limits could not be loaded. Reload to try again." : "Loading date limits…"}</p>}
        {!hasValidDateFormat && <p className="field-error field-wide" id="date-format-error">Enter real dates in YYYY-MM-DD format.</p>}
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
        <legend>Whole-trip budget <span>Required</span></legend>
        <p className="field-help">Provide the total amount for all travelers and its currency.</p>
        <div className="product-form-grid">
          <label>
            Budget amount
            <input
              type="number"
              value={budgetAmount}
              required
              min="0"
              step="0.01"
              disabled={isSubmitting}
              placeholder="2000"
              aria-describedby={!hasValidBudget ? "budget-error" : undefined}
              onChange={(event) => setBudgetAmount(event.target.value)}
            />
          </label>
          <CurrencySelect value={budgetCurrency} onChange={setBudgetCurrency}
            disabled={isSubmitting} describedBy={!hasValidBudget ? "budget-error" : undefined} />
          {!hasValidBudget && (
            <p className="field-error field-wide" id="budget-error">
              Enter a non-negative amount and select a currency.
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
          {isSubmitting ? "Building your itinerary…" : submitLabel || "Generate itinerary"}
        </button>
        <span className="form-note">Generation may take a moment.</span>
      </div>
    </form>
  );
}
