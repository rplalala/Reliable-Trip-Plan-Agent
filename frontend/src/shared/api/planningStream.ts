import { HttpError } from "./http";

export interface PlanningEvent {
  type: string;
  run_id: string;
  sequence: number;
  elapsed_ms: number;
  stage?: string;
  stage_id?: string;
  parent_id?: string | null;
  occurrence?: number;
  status?: string;
  message?: string;
  duration_ms?: number;
  details?: unknown;
  name?: string;
  dropped_events?: number;
  result?: unknown;
  http_status?: number;
  detail?: unknown;
}

/** Consume one request-lifetime stream. No automatic retries or reconnects. */
export async function planningStream<T>(
  url: string, input: unknown, signal: AbortSignal,
  onEvent: (event: PlanningEvent) => void,
): Promise<T> {
  const response = await fetch(url, {
    method: "POST", headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify(input), signal,
  });
  if (!response.ok) throw new HttpError(response.status, await response.json().catch(() => null));
  if (!response.body || !response.headers.get("content-type")?.includes("text/event-stream")) {
    throw new Error("Expected a planning event stream");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let runId: string | undefined;
  let sequence = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      signal.throwIfAborted();
      buffer += decoder.decode(value, { stream: !done });
      let boundary: RegExpExecArray | null;
      while ((boundary = /\r?\n\r?\n/.exec(buffer)) !== null) {
        const frame = buffer.slice(0, boundary.index);
        buffer = buffer.slice(boundary.index + boundary[0].length);
        const data = frame.split(/\r?\n/).filter(line => line.startsWith("data:"))
          .map(line => line.slice(5).trimStart()).join("\n");
        if (!data) continue;
        const event = JSON.parse(data) as PlanningEvent;
        if (!event.run_id || !Number.isInteger(event.sequence) || !event.type) {
          throw new Error("Invalid planning event");
        }
        runId ??= event.run_id;
        if (event.run_id !== runId) throw new Error("Mismatched planning run");
        if (event.sequence <= sequence) continue;
        sequence = event.sequence;
        onEvent(event);
        if (event.type === "result") return event.result as T;
        if (event.type === "error") throw new HttpError(event.http_status ?? 502, event.detail);
        if (event.type === "cancelled") throw new DOMException("Cancelled", "AbortError");
      }
      if (done) throw new Error("Planning stream ended before a final result");
      if (buffer.length > 8_000_000) throw new Error("Planning event is too large");
    }
  } finally {
    await reader.cancel().catch(() => undefined);
    reader.releaseLock();
  }
}
