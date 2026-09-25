"""Request-lifetime SSE delivery: no background jobs, persistence or resume tokens."""

import asyncio
import json
from contextlib import suppress

import anyio
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from backend.app.observability.progress import ProgressObserver, progress_scope


async def planning_events(operation, observer, *, heartbeat_seconds=15):
    """Own the producer task; disconnect/iterator closure cancels and awaits cleanup."""

    async def produce():
        with progress_scope(observer):
            try:
                result = await operation()
                payload = result.model_dump(mode="json")
            except asyncio.CancelledError:
                observer.emit("cancelled", status="cancelled")
                raise
            except HTTPException as exc:
                observer.emit("error", http_status=exc.status_code, detail=exc.detail)
            except TimeoutError:
                observer.emit("error", http_status=504, detail={"code": "planning_timeout"})
            except Exception:
                observer.emit(
                    "error",
                    http_status=502,
                    detail={
                        "code": "planning_failed",
                        "message": "The itinerary could not be generated. Please try again.",
                    },
                )
            else:
                observer.emit("result", result=payload)

    observer.emit("started")
    task = asyncio.create_task(produce())
    try:
        while True:
            try:
                event = await asyncio.wait_for(observer.next(), timeout=heartbeat_seconds)
            except TimeoutError:
                yield ": keep-alive\n\n"
                continue
            yield f"event: {event['type']}\ndata: {json.dumps(event, ensure_ascii=True)}\n\n"
            if event["type"] in {"result", "error", "cancelled"}:
                break
    finally:
        if not task.done():
            task.cancel()
        # Shield cleanup from the response cancellation scope. Await completion before returning.
        with anyio.CancelScope(shield=True):
            with suppress(asyncio.CancelledError):
                await asyncio.shield(task)


class PlanningStreamingResponse(StreamingResponse):
    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        finally:
            # A send failure can interrupt async-for while the generator is suspended at yield.
            with anyio.CancelScope(shield=True):
                await self.body_iterator.aclose()


def planning_stream(operation, *, developer=False, version=None):
    observer = ProgressObserver(developer=developer, version=version)
    return PlanningStreamingResponse(
        planning_events(operation, observer),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"},
    )
