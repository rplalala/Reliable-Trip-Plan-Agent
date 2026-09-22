export interface TripDateWindow {
  allowedStart: string;
  allowedEnd: string;
  maxTripDays: number;
}

// ISO calendar arithmetic, independent of the browser's time zone and DST.
export function addCalendarDays(value: string, days: number): string {
  const date = new Date(`${value}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

export function latestEndDate(start: string, window: TripDateWindow): string {
  if (!start) return window.allowedEnd;
  const durationEnd = addCalendarDays(start, window.maxTripDays - 1);
  return durationEnd < window.allowedEnd ? durationEnd : window.allowedEnd;
}

export function isDateWithinTripWindow(value: string, window: TripDateWindow): boolean {
  return value >= window.allowedStart && value <= window.allowedEnd;
}
