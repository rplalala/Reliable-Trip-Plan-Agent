import { describe, expect, it } from "vitest";
import { addCalendarDays, latestEndDate, isDateWithinTripWindow } from "./datePolicy";
const window = { allowedStart: "2026-09-20", allowedEnd: "2026-10-03", maxTripDays: 10 };
describe("server-authoritative date window", () => {
  it("keeps duration separate from the fourteen selectable dates", () => {
    expect(latestEndDate("2026-09-20", window)).toBe("2026-09-29");
    expect(latestEndDate("2026-09-24", window)).toBe("2026-10-03");
    expect(latestEndDate("2026-10-03", window)).toBe("2026-10-03");
    expect(isDateWithinTripWindow("2026-10-03", window)).toBe(true);
    expect(isDateWithinTripWindow("2026-10-04", window)).toBe(false);
    expect(isDateWithinTripWindow("2026-09-19", window)).toBe(false);
  });
  it("uses calendar arithmetic across DST and year boundaries", () => {
    expect(addCalendarDays("2026-09-27", 9)).toBe("2026-10-06");
    expect(addCalendarDays("2026-12-28", 9)).toBe("2027-01-06");
  });
});
