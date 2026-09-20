import { render, screen, within, cleanup } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { Itinerary, ReferenceRecommendation } from "../types";
import { ItineraryView } from "./ItineraryView";

const base: Itinerary = {
  destination: "Example city", start_date: "2026-09-21", end_date: "2026-09-21",
  days: [{ date: "2026-09-21", activities: [{
    activity_id: "a", title: "Primary visit", place_name: "Museum", location: null,
    start_time: "2026-09-21T10:00:00+10:00", end_time: "2026-09-21T11:00:00+10:00",
    estimated_cost: null, notes: null,
  }] }],
};
const suggestion: ReferenceRecommendation = {
  place_name: "Optional cafe", source_place_id: null, source_ref: null,
  reason: "An extra place to consider", associated_day: null, area: null, uncertainty: null,
};
afterEach(cleanup);
describe("Itinerary reference roles", () => {
  it.each([undefined, []])("hides empty and historical references", (references) => {
    render(<ItineraryView itinerary={{ ...base, reference_recommendations: references }} />);
    expect(screen.queryByRole("region", { name: "Optional reference recommendations" })).not.toBeInTheDocument();
    expect(screen.getByText("10:00–11:00")).toBeInTheDocument();
  });
  it("separates model suggestions from timed visits and committed costs", () => {
    render(<ItineraryView itinerary={{ ...base, reference_recommendations: [suggestion] }} />);
    const section = screen.getByRole("region", { name: "Optional reference recommendations" });
    expect(within(section).getByText("Optional cafe")).toBeInTheDocument();
    expect(within(section).getByText(/Model-generated suggestion; not live-verified/)).toBeInTheDocument();
    expect(within(section).getByText(/No bookings have been made/)).toBeInTheDocument();
    expect(within(section).queryByText(/10:00|Estimated cost|Suggested day/)).not.toBeInTheDocument();
    expect(within(section).getAllByRole("article")).toHaveLength(1);
  });
  it("shows grounded source context, optional association and uncertainty without debug IDs", () => {
    render(<ItineraryView itinerary={{ ...base, reference_recommendations: [{ ...suggestion,
      source_place_id: "canonical-id", source_ref: "google_places:canonical-id",
      associated_day: "2026-09-21", area: "Old district", uncertainty: "Opening hours unknown",
    }] }} />);
    expect(screen.getByText(/Linked to supplied place information/)).toBeInTheDocument();
    expect(screen.getByText("Suggested day: 2026-09-21")).toBeInTheDocument();
    expect(screen.getByText("Old district")).toBeInTheDocument();
    expect(screen.getByText("Opening hours unknown")).toBeInTheDocument();
    expect(screen.queryByText(/canonical-id/)).not.toBeInTheDocument();
  });
});
