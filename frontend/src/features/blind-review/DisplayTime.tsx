const fallbackZones = ["UTC", "Asia/Shanghai", "Australia/Sydney", "Europe/London", "America/New_York"];
const intl = Intl as typeof Intl & { supportedValuesOf?: (key: "timeZone") => string[] };
const zones = [...new Set([...fallbackZones, ...(intl.supportedValuesOf?.("timeZone") ?? [])])].sort();

export function TimeZonePicker({ value, onChange }: { value: string; onChange: (zone: string) => void }) {
  return <label className="time-zone">Time zone<select value={value} onChange={e => onChange(e.target.value)}>
    {zones.map(zone => <option key={zone} value={zone}>{zone}</option>)}
  </select></label>;
}

function formattedTime(value: string, zone: string): { text: string; notice?: string } {
  const match = /^(\d{4}-\d{2}-\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?(Z|[+-]\d{2}(?::?\d{2})?)?$/.exec(value);
  if (match && validDate(match[1]) && validClock(match[2], match[3], match[4])) {
    if (!match[5]) return { text: `${match[1]} ${match[2]}:${match[3]}`, notice: "Time zone not supplied; not converted" };
    const suppliedOffset = match[5];
    const offset = suppliedOffset === "Z" || suppliedOffset.includes(":") ? suppliedOffset :
      `${suppliedOffset.slice(0, 3)}:${suppliedOffset.slice(3) || "00"}`;
    const instant = new Date(value.replace(" ", "T").slice(0, -suppliedOffset.length) + offset);
    if (Number.isFinite(instant.getTime())) {
      const parts = new Intl.DateTimeFormat("en-GB", {
        timeZone: zone, year: "numeric", month: "2-digit", day: "2-digit",
        hour: "2-digit", minute: "2-digit", hourCycle: "h23",
      }).formatToParts(instant);
      const fields = Object.fromEntries(parts.map(p => [p.type, p.value]));
      return { text: `${fields.year.padStart(4, "0")}-${fields.month}-${fields.day} ${fields.hour}:${fields.minute}` };
    }
  }
  const clock = /^(\d{2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?$/.exec(value);
  if (clock && validClock(clock[1], clock[2], clock[3])) return { text: `${clock[1]}:${clock[2]}`, notice: "Time zone not supplied; not converted" };
  return { text: value, notice: "Time unavailable for conversion; original value retained" };
}

function validClock(hour: string, minute: string, second = "0"): boolean {
  return Number(hour) < 24 && Number(minute) < 60 && Number(second) < 60;
}

function validDate(date: string): boolean {
  const [year, month, day] = date.split("-").map(Number);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return year > 0 && month >= 1 && month <= 12 && day >= 1 && day <= days[month - 1];
}

export function DisplayTime({ value, zone }: { value: unknown; zone: string }) {
  if (value === null || value === undefined) return <>Not supplied</>;
  if (typeof value !== "string") return <>{JSON.stringify(value)} <span className="uncertainty">Time unavailable for conversion</span></>;
  const result = formattedTime(value, zone);
  return <><span>{result.text}</span>{result.notice && <p className="uncertainty">{result.notice}</p>}</>;
}
