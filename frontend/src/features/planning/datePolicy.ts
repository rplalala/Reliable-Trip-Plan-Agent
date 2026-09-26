export interface TripDateWindow {
  allowedStart: string;
  allowedEnd: string;
  maxTripDays: number;
}

export function isValidISODate(value: string): boolean {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const year = Number(value.slice(0, 4));
  const month = Number(value.slice(5, 7));
  const day = Number(value.slice(8, 10));
  if (year < 1 || month < 1 || month > 12 || day < 1) return false;
  const lastDay = new Date(Date.UTC(year, month, 0)).getUTCDate();
  return day <= lastDay;
}

// ISO calendar arithmetic, independent of the browser's time zone and DST.
export function addCalendarDays(value: string, days: number): string {
  const date = new Date(`${value}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

export function latestEndDate(start: string, window: TripDateWindow): string {
  if (!isValidISODate(start)) return window.allowedEnd;
  const durationEnd = addCalendarDays(start, window.maxTripDays - 1);
  return durationEnd < window.allowedEnd ? durationEnd : window.allowedEnd;
}

export function isDateWithinTripWindow(value: string, window: TripDateWindow): boolean {
  return isValidISODate(value) && value >= window.allowedStart && value <= window.allowedEnd;
}
