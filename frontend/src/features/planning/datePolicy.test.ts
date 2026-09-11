import { describe, expect, it } from "vitest";

import {
  addBrowserLocalCalendarDays,
  getBrowserLocalDate,
  getBrowserLocalTripDateWindow,
  isDateWithinTripWindow,
} from "./datePolicy";

describe("browser-local trip date policy", () => {
  it("formats browser-local calendar fields without UTC conversion", () => {
    const localDate = {
      getFullYear: () => 2026,
      getMonth: () => 8,
      getDate: () => 7,
      toISOString: () => {
        throw new Error("UTC conversion must not be used");
      },
    } as unknown as Date;

    expect(getBrowserLocalDate(localDate)).toBe("2026-09-07");
  });

  it("computes an inclusive ten-day window across a month boundary", () => {
    const window = getBrowserLocalTripDateWindow(new Date(2026, 8, 25, 12));

    expect(window).toEqual({
      allowedStart: "2026-09-25",
      allowedEnd: "2026-10-04",
    });
  });

  it("adds calendar days while preserving local calendar semantics", () => {
    const result = addBrowserLocalCalendarDays(new Date(2026, 11, 28, 12), 9);

    expect(getBrowserLocalDate(result)).toBe("2027-01-06");
    expect(result.getHours()).toBe(12);
  });

  it("accepts only dates inside the inclusive window", () => {
    const window = {
      allowedStart: "2026-09-11",
      allowedEnd: "2026-09-20",
    };

    expect(isDateWithinTripWindow("2026-09-11", window)).toBe(true);
    expect(isDateWithinTripWindow("2026-09-20", window)).toBe(true);
    expect(isDateWithinTripWindow("2026-09-10", window)).toBe(false);
    expect(isDateWithinTripWindow("2026-09-21", window)).toBe(false);
  });
});
