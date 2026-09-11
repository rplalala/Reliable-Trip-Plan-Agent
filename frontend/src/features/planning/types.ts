export interface Money {
  amount: string;
  currency: string;
}

export interface TravelRequirements {
  destination: string | null;
  start_date: string | null;
  end_date: string | null;
  traveler_count: number | null;
  budget: Money | null;
  required_activities: string[];
  excluded_activities: string[];
  preferences: string[];
  unresolved_fields: string[];
}

export interface Activity {
  activity_id: string;
  title: string;
  place_name: string | null;
  location: string | null;
  start_time: string;
  end_time: string;
  estimated_cost: Money | null;
  notes: string | null;
}

export interface ItineraryDay {
  date: string;
  activities: Activity[];
}

export interface Itinerary {
  destination: string;
  start_date: string;
  end_date: string;
  days: ItineraryDay[];
}

export interface ProductPlanningInput {
  destination: string;
  start_date: string;
  end_date: string;
  traveler_count: number;
  budget?: Money;
  additional_preferences?: string;
}

export interface CompletedPlanningResponse {
  status: "completed";
  requirements: TravelRequirements;
  itinerary: Itinerary;
}

export interface NeedsClarificationResponse {
  status: "needs_clarification";
  requirements: TravelRequirements;
}

export type ProductPlanningResponse =
  | CompletedPlanningResponse
  | NeedsClarificationResponse;
