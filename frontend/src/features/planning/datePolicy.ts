export const TRIP_DATE_WINDOW_DAYS = 10;

export interface BrowserLocalTripDateWindow {
  allowedStart: string;
  allowedEnd: string;
}

export function getBrowserLocalDate(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function addBrowserLocalCalendarDays(date: Date, days: number): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + days, 12);
}

export function getBrowserLocalTripDateWindow(
  referenceDate = new Date(),
): BrowserLocalTripDateWindow {
  return {
    allowedStart: getBrowserLocalDate(referenceDate),
    allowedEnd: getBrowserLocalDate(
      addBrowserLocalCalendarDays(referenceDate, TRIP_DATE_WINDOW_DAYS - 1),
    ),
  };
}

export function isDateWithinTripWindow(
  value: string,
  window: BrowserLocalTripDateWindow,
): boolean {
  return value >= window.allowedStart && value <= window.allowedEnd;
}
