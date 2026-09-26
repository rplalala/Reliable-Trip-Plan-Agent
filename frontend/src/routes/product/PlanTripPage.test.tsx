import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getTripDateWindow, submitPlanningRequest } from "../../features/planning/api";
import type { ProductPlanningResponse } from "../../features/planning/types";
import { PlanTripPage } from "./PlanTripPage";

vi.mock("../../features/planning/api", () => ({
  submitPlanningRequest: vi.fn(),
  getTripDateWindow: vi.fn(),
  getDestinationSuggestions: vi.fn().mockResolvedValue({ source: "geodb", suggestions: [] }),
}));

const submitPlanningMock = vi.mocked(submitPlanningRequest);

const completedResult: ProductPlanningResponse = {
  status: "completed",
  requirements: {
    destination: "Kyoto",
    start_date: "2026-09-12",
    end_date: "2026-09-12",
    traveler_count: 1,
    budget: null,
    required_activities: [],
    excluded_activities: [],
    preferences: [],
    unresolved_fields: [],
  },
  itinerary: {
    destination: "Kyoto",
    start_date: "2026-09-12",
    end_date: "2026-09-12",
    days: [
      {
        date: "2026-09-12",
        activities: [
          {
            activity_id: "activity-1",
            title: "Visit Fushimi Inari Shrine",
            place_name: "Fushimi Inari Taisha",
            location: "Kyoto",
            start_time: "2026-09-12T09:00:00+09:00",
            end_time: "2026-09-12T11:00:00+09:00",
            estimated_cost: null,
            notes: null,
          },
        ],
      },
    ],
  },
};

type TestUser = ReturnType<typeof userEvent.setup>;

async function fillRequiredFields(user: TestUser, withBudget = true) {
  await user.type(screen.getByLabelText("Destination"), "Kyoto");
  await user.type(screen.getByLabelText("Start date"), "2026-09-12");
  await user.type(screen.getByLabelText("End date"), "2026-09-12");
  await user.type(screen.getByLabelText("Travelers"), "1");
  if (withBudget) {
    await user.type(screen.getByLabelText("Budget amount"), "2000");
  }
}

describe("PlanTripPage", () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date(2026, 8, 11, 12));
    submitPlanningMock.mockReset();
    vi.mocked(getTripDateWindow).mockResolvedValue({allowedStart: "2026-09-11", allowedEnd: "2026-09-24", maxTripDays: 10});
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("defaults currency to AUD and filters selectable currencies by name", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    expect(screen.getByRole("combobox", { name: "Currency" })).toHaveValue("AUD");
    await user.type(screen.getByRole("searchbox", { name: "Search currencies" }), "New Zealand");
    expect(screen.getByRole("option", { name: /NZD.*New Zealand dollar/ })).toBeInTheDocument();
    expect(screen.queryByRole("option", { name: /USD.*US dollar/ })).toBeNull();
    await user.selectOptions(screen.getByRole("combobox", { name: "Currency" }), "NZD");
    expect(screen.getByRole("combobox", { name: "Currency" })).toHaveValue("NZD");
  });

  it("does not submit a rolled-over or partial calendar date", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await user.type(screen.getByLabelText("Destination"), "Kyoto");
    fireEvent.change(screen.getByLabelText("Start date"), { target: { value: "2026-09-31" } });
    fireEvent.change(screen.getByLabelText("End date"), { target: { value: "2026-09-31" } });
    await user.type(screen.getByLabelText("Travelers"), "1");
    await user.type(screen.getByLabelText("Budget amount"), "2000");
    expect(screen.getByText("Enter real dates in YYYY-MM-DD format.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Start date"), { target: { value: "2026-09" } });
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("shows provider filtering separately and waits for manual resubmission", async () => {
    submitPlanningMock.mockResolvedValue({
      status: "provider_blocked",
      message: "Your preference input triggered the AI provider's content filter.",
      action: "Please rewrite your preferences as travel-related requests and submit again.",
    });
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText("Please revise your preferences")).toBeInTheDocument();
    expect(screen.getByText(/provider's content filter/)).toBeInTheDocument();
    expect(submitPlanningMock).toHaveBeenCalledTimes(1);
    expect(screen.queryByText("Travel planning paused")).not.toBeInTheDocument();
    await user.type(screen.getByLabelText("Destination"), " City");
    expect(screen.queryByText("Please revise your preferences")).not.toBeInTheDocument();
  });

  it("requires structured trip fields before enabling submission", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);

    const submitButton = screen.getByRole("button", { name: "Generate itinerary" });
    expect(submitButton).toBeDisabled();

    await fillRequiredFields(user);

    expect(submitButton).toBeEnabled();
  });

  it("blocks an invalid date range", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);

    await user.type(screen.getByLabelText("Destination"), "Kyoto");
    await user.type(screen.getByLabelText("Start date"), "2026-09-14");
    await user.type(screen.getByLabelText("End date"), "2026-09-12");
    await user.type(screen.getByLabelText("Travelers"), "1");

    expect(screen.getByText("End date must be on or after the start date.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("limits both date pickers to the server-authoritative fourteen-date window", async () => {
    render(<PlanTripPage />);

    await screen.findByText("Generate itinerary");
    await act(async () => {});
    expect(screen.getByLabelText("Start date")).toHaveAttribute("min", "2026-09-11");
    expect(screen.getByLabelText("Start date")).toHaveAttribute("max", "2026-09-24");
    expect(screen.getByLabelText("End date")).toHaveAttribute("min", "2026-09-11");
    expect(screen.getByLabelText("End date")).toHaveAttribute("max", "2026-09-24");
  });

  it("blocks a date outside the server-authoritative fourteen-date window", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);

    await user.type(screen.getByLabelText("Destination"), "Kyoto");
    fireEvent.change(screen.getByLabelText("Start date"), {
      target: { value: "2026-09-26" },
    });
    fireEvent.change(screen.getByLabelText("End date"), {
      target: { value: "2026-09-26" },
    });
    await user.type(screen.getByLabelText("Travelers"), "1");

    expect(
      screen.getByText("Travel dates must be between 2026-09-11 and 2026-09-24."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("requires a complete valid budget pair", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user, false);
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();

    await user.type(screen.getByLabelText("Budget amount"), "2000");
    expect(screen.getByRole("combobox", { name: "Currency" })).toHaveValue("AUD");
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeEnabled();
  });

  it("rejects a negative budget amount", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user, false);

    await user.type(screen.getByLabelText("Budget amount"), "-1");

    expect(
      screen.getByText("Enter a non-negative amount and select a currency."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("submits explicit fields and renders a completed itinerary", async () => {
    submitPlanningMock.mockResolvedValue(completedResult);
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user, false);
    await user.type(screen.getByLabelText("Budget amount"), "2000");
    await user.selectOptions(screen.getByRole("combobox", { name: "Currency" }), "NZD");
    await user.type(
      screen.getByLabelText("Additional preferences Optional"),
      "Local food and quiet mornings.",
    );

    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(submitPlanningMock).toHaveBeenCalledWith({
      destination: "Kyoto",
      start_date: "2026-09-12",
      end_date: "2026-09-12",
      traveler_count: 1,
      budget: { amount: "2000", currency: "NZD" },
      additional_preferences: "Local food and quiet mornings.",
    }, expect.objectContaining({ signal: expect.any(AbortSignal), onEvent: expect.any(Function) }));
    expect(await screen.findByRole("heading", { name: "Kyoto" })).toBeInTheDocument();
    expect(screen.getByText("Visit Fushimi Inari Shrine")).toBeInTheDocument();
    expect(screen.getByRole("combobox", { name: "Currency" })).toHaveValue("NZD");
    expect(screen.queryByText(/V0|V1|V2|V3/)).not.toBeInTheDocument();
  });

  it("clears an adopted result when currency or calendar date changes", async () => {
    submitPlanningMock.mockResolvedValue(completedResult);
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText("Visit Fushimi Inari Shrine")).toBeInTheDocument();
    await user.selectOptions(screen.getByRole("combobox", { name: "Currency" }), "NZD");
    expect(screen.queryByText("Visit Fushimi Inari Shrine")).toBeNull();
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText("Visit Fushimi Inari Shrine")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Choose Start date" }));
    await user.click(screen.getByRole("button", { name: "September 13, 2026" }));
    expect(screen.getByLabelText("Start date")).toHaveValue("2026-09-13");
    expect(screen.queryByText("Visit Fushimi Inari Shrine")).toBeNull();
  });

  it("keeps an incomplete itinerary visible without claiming it is ready", async () => {
    submitPlanningMock.mockResolvedValue({
      ...completedResult,
      policy_completion: "incomplete",
      policy_reasons: ["required_visit_obligation_unmet"],
    });
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(await screen.findByText("Visit Fushimi Inari Shrine")).toBeInTheDocument();
    expect(screen.getByText(/This itinerary is incomplete/)).toBeInTheDocument();
    expect(screen.getByText(/Planning finished with unmet requirements/)).toHaveAttribute("role", "status");
    expect(screen.queryByText("Your itinerary is ready")).not.toBeInTheDocument();
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "1");
  });

  it("omits blank optional Product fields", async () => {
    submitPlanningMock.mockResolvedValue(completedResult);
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.type(screen.getByLabelText("Additional preferences Optional"), "   ");

    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(submitPlanningMock).toHaveBeenCalledWith({
      destination: "Kyoto",
      start_date: "2026-09-12",
      end_date: "2026-09-12",
      traveler_count: 1,
      budget: { amount: "2000", currency: "AUD" },
    }, expect.objectContaining({ signal: expect.any(AbortSignal) }));
  });

  it("uses a neutral message for the defensive clarification outcome", async () => {
    submitPlanningMock.mockResolvedValue({
      status: "needs_clarification",
      requirements: {
        ...completedResult.requirements,
        start_date: null,
        unresolved_fields: ["start_date"],
      },
    });
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);

    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(
      await screen.findByText("We couldn't interpret some of your trip details"),
    ).toBeInTheDocument();
    expect(screen.getByText("Please review them and try again.")).toBeInTheDocument();
    expect(screen.queryByText("start date")).not.toBeInTheDocument();
  });

  it("shows exact text safely, retains fields, and clears issues on edit and resubmit", async () => {
    const quote = '<img src=x onerror="alert(1)"> Visit New York.';
    submitPlanningMock.mockResolvedValueOnce({
      status: "needs_clarification",
      requirements: completedResult.requirements,
      issues: {
        input_disposition: "REWRITE_REQUIRED",
        issues: [{
          issue_type: "destination_scope_conflict",
          source_refs: [{ quote, start: 0, end: quote.length }],
          quote_status: "located", related_field: "destination", current_value: "Kyoto",
          reason: "This requests a different physical trip scope.",
          action: "Update the destination or revise the requested visit.",
        }],
      },
    }).mockResolvedValueOnce(completedResult);
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    const preference = screen.getByLabelText("Additional preferences Optional");
    await user.type(preference, quote);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText(quote, { selector: "blockquote" })).toBeInTheDocument();
    expect(document.querySelector("blockquote img")).toBeNull();
    expect(screen.getByText("Current destination: Kyoto")).toBeInTheDocument();
    expect(preference).toHaveValue(quote);
    await user.clear(preference);
    await user.type(preference, "Local museums.");
    expect(screen.queryByText("This requests a different physical trip scope.")).toBeNull();
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(submitPlanningMock).toHaveBeenLastCalledWith(expect.objectContaining({
      additional_preferences: "Local museums.", destination: "Kyoto",
    }), expect.objectContaining({ signal: expect.any(AbortSignal) }));
  });

  it("uses dedicated safety presentation and removes old safety and itinerary results", async () => {
    submitPlanningMock.mockResolvedValueOnce(completedResult).mockResolvedValueOnce({
      status: "safety_blocked", requirements: completedResult.requirements,
      message: "Your safety matters. Travel planning has been paused.",
      action: "Please seek support from someone you trust.",
    });
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    const preference = screen.getByLabelText("Additional preferences Optional");
    await user.type(preference, "Changed request");
    expect(document.querySelector(".itinerary")).toBeNull();
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText("Travel planning paused")).toBeInTheDocument();
    expect(screen.queryByText("We couldn't interpret some of your trip details")).toBeNull();
    await user.clear(preference);
    expect(screen.queryByText("Travel planning paused")).toBeNull();
  });

  it("renders unavailable quotes without fabricating source text", async () => {
    submitPlanningMock.mockResolvedValue({
      status: "needs_clarification", requirements: completedResult.requirements,
      issues: { issues: [{
        issue_type: "structured_request_conflict", source_refs: [], quote_status: "unavailable",
        related_field: "destination", current_value: "Kyoto",
        reason: "Conflicting destination.", action: "Review the destination field.",
      }] },
    });
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(await screen.findByText("Original quote unavailable.")).toBeInTheDocument();
    expect(document.querySelector("blockquote")).toBeNull();
    expect(screen.getByText("Review the destination field.")).toBeInTheDocument();
  });

  it("shows a product-safe failure message", async () => {
    submitPlanningMock.mockRejectedValue(new Error("provider secret"));
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);

    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(
      await screen.findByText("We could not generate your itinerary. Please try again."),
    ).toBeInTheDocument();
    expect(screen.queryByText("provider secret")).not.toBeInTheDocument();
  });

  it("disables repeat submission while planning is in progress", async () => {
    let resolvePlanning: (value: ProductPlanningResponse) => void = () => undefined;
    submitPlanningMock.mockReturnValue(
      new Promise((resolve) => {
        resolvePlanning = resolve;
      }),
    );
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);

    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));

    expect(screen.getByRole("button", { name: "Building your itinerary…" })).toBeDisabled();
    expect(submitPlanningMock).toHaveBeenCalledOnce();

    await act(async () => {
      resolvePlanning(completedResult);
    });
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeEnabled();
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "1");
    expect(screen.getByRole("status")).toHaveTextContent("Your itinerary is ready");
  });

  it("shows stage-driven safe progress and ignores a stopped run's late result", async () => {
    let resolve!: (value: ProductPlanningResponse) => void;
    submitPlanningMock.mockImplementation(() => new Promise(yes => { resolve = yes; }));
    const user = userEvent.setup();
    const { unmount } = render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    const options = submitPlanningMock.mock.calls[0][1]!;
    act(() => options.onEvent({ type: "stage", run_id: "one", sequence: 1, elapsed_ms: 10,
      stage: "weather", status: "started", message: "Checking the weather", details: { provider: "secret debug" } }));
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "0.32");
    expect(screen.getByRole("status")).toHaveTextContent("Checking the weather");
    expect(screen.queryByText(/secret debug/)).toBeNull();
    for (const [stage, message] of [["repair", "Adjusting your itinerary"], ["official_information", "Checking place information"]]) {
      act(() => options.onEvent({ type: "stage", run_id: "one", sequence: 2, elapsed_ms: 20,
        stage, status: "skipped", message }));
      expect(screen.getByRole("status")).toHaveTextContent("Checking the weather");
      expect(screen.queryByText(message)).toBeNull();
    }
    act(() => options.onEvent({ type: "stage", run_id: "one", sequence: 4, elapsed_ms: 30,
      stage: "generation", status: "started", message: "Planning your days" }));
    expect(screen.getByRole("status")).toHaveTextContent("Planning your days");
    await user.click(screen.getByRole("button", { name: "Stop planning" }));
    expect(options.signal.aborted).toBe(true);
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "0.5");
    await act(async () => resolve(completedResult));
    expect(screen.queryByRole("heading", { name: "Kyoto" })).toBeNull();
    await user.click(screen.getByRole("button", { name: "Generate itinerary" }));
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "0");
    const next = submitPlanningMock.mock.calls[1][1]!;
    unmount();
    expect(next.signal.aborted).toBe(true);
  });
});

 it("limits the selected trip to ten inclusive days", async () => {
   vi.mocked(getTripDateWindow).mockResolvedValue({allowedStart: "2026-09-20", allowedEnd: "2026-10-03", maxTripDays: 10});
   render(<PlanTripPage />);
   await act(async () => {});
   fireEvent.change(screen.getByLabelText("Start date"), {target:{value:"2026-09-20"}});
   expect(screen.getByLabelText("End date")).toHaveAttribute("max", "2026-09-29");
   fireEvent.change(screen.getByLabelText("End date"), {target:{value:"2026-09-30"}});
   expect(screen.getByText(/Trips may last at most 10 days/)).toBeInTheDocument();
   expect(screen.getByRole("button", {name:"Generate itinerary"})).toBeDisabled();
 });
