import { afterEach, describe, expect, it, vi } from "vitest";
import { planningStream } from "./planningStream";

afterEach(() => vi.unstubAllGlobals());
function response(chunks: string[]) {
  const bytes = new TextEncoder().encode(chunks.join(""));
  return new Response(new ReadableStream({ start(controller) {
    // Split every UTF-8 byte, including within multibyte characters and delimiters.
    bytes.forEach(byte => controller.enqueue(new Uint8Array([byte])));
    controller.close();
  } }), { headers: { "Content-Type": "text/event-stream" } });
}
const frame = (type: string, sequence: number, extra = {}) => `event: ${type}\r\ndata: ${JSON.stringify({ type, sequence, run_id: "one", elapsed_ms: 20, ...extra })}\r\n\r\n`;
describe("planning stream transport", () => {
  it("handles split UTF-8, heartbeats, duplicate sequences and a terminal result", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response([
      ": keep-alive\r\n\r\n", frame("stage", 1, { message: "Café" }), frame("stage", 1),
      frame("result", 3, { result: { status: "completed" } }),
    ])));
    const callback = vi.fn();
    expect(await planningStream("/stream", {}, new AbortController().signal, callback)).toEqual({ status: "completed" });
    expect(callback).toHaveBeenCalledTimes(2);
    expect(callback.mock.calls[0][0].message).toBe("Café");
  });
  it.each([
    [frame("stage", 1), "before a final result"],
    [frame("stage", 1) + frame("result", 2, { run_id: "other" }), "Mismatched planning run"],
    ["data: invalid\n\n", "JSON"],
  ])("rejects interrupted or invalid streams", async (data, message) => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response([data])));
    await expect(planningStream("/stream", {}, new AbortController().signal, vi.fn())).rejects.toThrow(message);
  });
  it("preserves direct validation and in-stream HTTP errors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ detail: "invalid" }), { status: 422 }))
      .mockResolvedValueOnce(response([frame("error", 1, { http_status: 504, detail: { code: "planning_timeout" } })])));
    await expect(planningStream("/stream", {}, new AbortController().signal, vi.fn())).rejects.toMatchObject({ status: 422 });
    await expect(planningStream("/stream", {}, new AbortController().signal, vi.fn())).rejects.toMatchObject({ status: 504 });
  });
  it("does not deliver buffered results after cancellation", async () => {
    const controller = new AbortController(); controller.abort();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response([frame("result", 1, { result: {} })])));
    const callback = vi.fn();
    await expect(planningStream("/stream", {}, controller.signal, callback)).rejects.toMatchObject({ name: "AbortError" });
    expect(callback).not.toHaveBeenCalled();
  });
});
