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
  source_place_id?: string | null;
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

export interface ReferenceRecommendation {
  place_name: string;
  source_place_id: string | null;
  reason: string;
  associated_day: string | null;
  area: string | null;
  uncertainty: string | null;
  source_ref: string | null;
}

export interface Itinerary {
  output_version?: "itinerary_1" | "itinerary_2";
  reference_recommendations?: ReferenceRecommendation[];
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
