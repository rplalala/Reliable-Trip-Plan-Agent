export type DeveloperVersion = "v0";

export interface DeveloperPlanningRequest {
  version: DeveloperVersion;
  request_text: string;
  reference_date: string;
}
