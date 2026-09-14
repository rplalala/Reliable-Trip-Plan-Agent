import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { submitPlanningRequest } from "../../features/planning/api";
import type { ProductPlanningResponse } from "../../features/planning/types";
import { PlanTripPage } from "./PlanTripPage";

vi.mock("../../features/planning/api", () => ({
  submitPlanningRequest: vi.fn(),
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

async function fillRequiredFields(user: TestUser) {
  await user.type(screen.getByLabelText("Destination"), "Kyoto");
  await user.type(screen.getByLabelText("Start date"), "2026-09-12");
  await user.type(screen.getByLabelText("End date"), "2026-09-12");
  await user.type(screen.getByLabelText("Travelers"), "1");
}

describe("PlanTripPage", () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date(2026, 8, 11, 12));
    submitPlanningMock.mockReset();
  });

  afterEach(() => {
    vi.useRealTimers();
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

  it("limits both date pickers to the browser-local ten-day window", () => {
    render(<PlanTripPage />);

    expect(screen.getByLabelText("Start date")).toHaveAttribute("min", "2026-09-11");
    expect(screen.getByLabelText("Start date")).toHaveAttribute("max", "2026-09-20");
    expect(screen.getByLabelText("End date")).toHaveAttribute("min", "2026-09-11");
    expect(screen.getByLabelText("End date")).toHaveAttribute("max", "2026-09-20");
  });

  it("blocks a date outside the browser-local ten-day window", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);

    await user.type(screen.getByLabelText("Destination"), "Kyoto");
    fireEvent.change(screen.getByLabelText("Start date"), {
      target: { value: "2026-09-21" },
    });
    fireEvent.change(screen.getByLabelText("End date"), {
      target: { value: "2026-09-21" },
    });
    await user.type(screen.getByLabelText("Travelers"), "1");

    expect(
      screen.getByText("Travel dates must be between 2026-09-11 and 2026-09-20."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("requires a complete valid budget pair", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);

    await user.type(screen.getByLabelText("Budget amount"), "2000");
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();

    await user.type(screen.getByLabelText("Currency"), "aud");
    expect(
      screen.getByText("Enter a non-negative amount and a three-letter uppercase currency code."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();

    await user.clear(screen.getByLabelText("Currency"));
    await user.type(screen.getByLabelText("Currency"), "AUD");
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeEnabled();
  });

  it("rejects a negative budget amount", async () => {
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);

    await user.type(screen.getByLabelText("Budget amount"), "-1");
    await user.type(screen.getByLabelText("Currency"), "AUD");

    expect(
      screen.getByText("Enter a non-negative amount and a three-letter uppercase currency code."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate itinerary" })).toBeDisabled();
  });

  it("submits explicit fields and renders a completed itinerary", async () => {
    submitPlanningMock.mockResolvedValue(completedResult);
    const user = userEvent.setup();
    render(<PlanTripPage />);
    await fillRequiredFields(user);
    await user.type(screen.getByLabelText("Budget amount"), "2000");
    await user.type(screen.getByLabelText("Currency"), "AUD");
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
      budget: { amount: "2000", currency: "AUD" },
      additional_preferences: "Local food and quiet mornings.",
    });
    expect(await screen.findByRole("heading", { name: "Kyoto" })).toBeInTheDocument();
    expect(screen.getByText("Visit Fushimi Inari Shrine")).toBeInTheDocument();
    expect(screen.queryByRole("combobox")).not.toBeInTheDocument();
    expect(screen.queryByText(/V0|V1|V2|V3/)).not.toBeInTheDocument();
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
    });
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
  });
});
