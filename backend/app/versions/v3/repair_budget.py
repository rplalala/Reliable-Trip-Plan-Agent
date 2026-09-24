"""One repair ledger and monotonic deadline; local exhaustion is not global failure."""

import asyncio
from collections import Counter
from time import monotonic

from backend.app.runtime.cache import RequestCache


def configured_policy():
    from backend.app.runtime.config_loader import load_runtime_config

    policy = load_runtime_config().v3_repair
    if policy is None:
        raise ValueError("runtime.v3_repair is required for V3")
    return policy


class RepairLimit(RuntimeError):
    pass


class RepairBudget:
    def __init__(
        self,
        request_deadline,
        *,
        clock=monotonic,
        cache=None,
        policy=None,
        nearby_reserve=None,
        runtime_config=None,
    ):
        from backend.app.runtime.config_loader import load_runtime_config

        runtime_config = runtime_config if runtime_config is not None else load_runtime_config()
        self.rag_config = runtime_config.tripworld_discovery
        self.policy = policy if policy is not None else configured_policy()
        if nearby_reserve is None:
            nearby_reserve = runtime_config.reference_discovery.deadline_seconds
        self.limits = self.policy.acquisition.model_dump(
            include={
                "google",
                "fallback",
                "embedding",
                "retrieval",
                "canonical",
                "details",
                "routes",
                "elements",
            }
        ) | {"model": self.policy.max_model_calls}
        self.clock = clock
        self.started = clock()
        self.deadline = min(
            self.started + self.policy.timing.stage_seconds, request_deadline - nearby_reserve
        )
        self.io_deadline = self.deadline
        self.used = Counter()
        self.stops = []
        self.cache = cache if cache is not None else RequestCache()
        # A new phase is not a retry opportunity, including failed pre-send attempts.
        # This does not relabel a reservation as a send or consume the new send budget.
        self.attempted = set(self.cache.attempts)

    def remaining(self):
        return max(0, self.deadline - self.clock())

    def charge(self, **charges):
        for key, amount in charges.items():
            if amount < 0 or self.used[key] + amount > self.limits[key]:
                raise RepairLimit(f"{key}_exhausted")
        self.used.update(charges)

    async def call(self, key, factory, *, charges, timeout=None, observed=False, unwrap=False):
        """Reuse compatible cache entries; charge failed sends, never retry a key.

        observed=True requires the provider's actual send notification. For fixture or
        non-observing ports, dispatch is conservatively counted as a send attempt.
        """
        cached, hit = self.cache.lookup(key)
        if hit:
            self.used["cache_hits"] += 1
            return getattr(cached, "value", cached) if unwrap else cached
        if key in self.attempted or self.cache.terminal_attempt(key):
            self.stops.append("previous_attempt")
            return None
        available = min(self.remaining(), self.io_deadline - self.clock())
        if available <= 0:
            self.stops.append("phase_deadline")
            return None
        self.attempted.add(key)
        try:

            async def load():
                async with asyncio.timeout(
                    min(timeout or self.policy.acquisition.provider_timeout_seconds, available)
                ):
                    value = await self.cache.dispatch(
                        key, factory, on_send=lambda: self.charge(**charges), observed=observed
                    )
                    if unwrap:
                        from backend.app.services.evidence_acquisition import _ProviderResult

                        return _ProviderResult(value=value)
                    return value

            value, _ = await self.cache.get_or_create(key, load)
            return getattr(value, "value", value) if unwrap else value
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.stops.append(f"{key[0]}:{type(exc).__name__}")
            return None
