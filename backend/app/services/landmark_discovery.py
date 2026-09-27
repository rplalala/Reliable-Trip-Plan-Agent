"""Allocate discovery inside the existing search pool and resolve nomination identity."""

from backend.app.evidence.selection_models import PlaceSearchIntent, SearchIntentKind
from backend.app.policies.poi_funnel import resolve_named_place_intents
from backend.app.runtime.budget import ToolBudgetKey
from backend.app.schemas.landmark_nomination import LandmarkIdentity
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent


class LandmarkDiscovery:
    def __init__(self, acquisition, nomination):
        self.acquisition, self.nomination = acquisition, nomination
        self.report = {}

    def resolutions(self, observations):
        names = [
            NamedPlaceIntent(
                place_text=name, source_text=name, inclusion=NamedPlaceInclusion.OPTIONAL
            )
            for name in self.nomination.names
        ]
        return resolve_named_place_intents(names, (), observations)

    async def search(self, contract, destination, intents, failures, executions):
        acq = self.acquisition
        names = await self.nomination.nominate(destination.model_dump(mode="json"))
        named = [i for i in intents if i.named_place_intent is not None]
        general = next((i for i in intents if i.intent_id == "default_0"), None)
        if general is None:
            general = PlaceSearchIntent(
                intent_id="default_0",
                term="top attractions",
                query=f"top attractions in {contract.requirements.destination}",
                kind=SearchIntentKind.FALLBACK,
            )
            intents.append(general)
        pending = [i for i in intents if i not in named and i is not general]
        observations = []
        self.report = dict(
            supplementary_sends=0,
            resolved=0,
            unresolved=len(names),
            general_status="not_attempted",
            status="started",
        )

        async def search(items):
            if items:
                observations.extend(
                    await acq.search_candidate_observations(
                        contract.requirements,
                        destination,
                        intents=items,
                        failed_intent_ids=failures,
                        intent_executions=executions,
                    )
                )

        try:
            await search(named)
            await search([general])
            self.report["general_status"] = next(
                e.status for e in executions if e.intent_id == general.intent_id
            )
            reserve = min(
                self.nomination.config.supplementary_searches,
                sum(r.resolved_place_id is None for r in self.resolutions(observations)),
            )
            while pending and acq._budget.remaining(ToolBudgetKey.CANDIDATE_SEARCH_CALLS) > reserve:
                await search([pending.pop(0)])
            reused = {
                r.resolved_place_id for r in self.resolutions(observations) if r.resolved_place_id
            }
            self.report["reused"] = len(reused)
            for index in range(len(names)):
                resolution = self.resolutions(observations)[index]
                # Ambiguous identities cannot be fixed by choosing the first query hit.
                if resolution.matching_place_ids:
                    continue
                if (
                    self.report["supplementary_sends"]
                    >= self.nomination.config.supplementary_searches
                ):
                    self.report["supplementary_stop"] = "supplementary_limit"
                    break
                intent = PlaceSearchIntent(
                    intent_id=f"landmark_{index + 1}",
                    term=names[index],
                    query=f"{names[index]} in {contract.requirements.destination}",
                    kind=SearchIntentKind.FALLBACK,
                )
                intents.append(intent)
                before = acq._budget.remaining(ToolBudgetKey.CANDIDATE_SEARCH_CALLS)
                try:
                    await search([intent])
                finally:
                    self.report["supplementary_sends"] += before - acq._budget.remaining(
                        ToolBudgetKey.CANDIDATE_SEARCH_CALLS
                    )
                if executions[-1].status == "budget_not_attempted":
                    self.report["supplementary_stop"] = "shared_search_limit"
                    break
            # Unspent reserved opportunities return to ordinary discovery.
            await search(pending)
            self.report["status"] = "completed"
        except BaseException:
            self.report["status"] = "interrupted"
            raise
        finally:
            resolutions = self.resolutions(observations)
            self.report.update(
                resolved=sum(r.resolved_place_id is not None for r in resolutions),
                unresolved=sum(r.resolved_place_id is None for r in resolutions),
                nomination_status=self.nomination.record["status"],
                candidate_search_sends=acq._budget.summary()[
                    ToolBudgetKey.CANDIDATE_SEARCH_CALLS.value
                ]["used"],
            )
            if self.report["status"] == "completed" and not self.report["resolved"]:
                self.report["status"] = "degraded"
            acq.landmark_diagnostics = dict(self.report)
            if self.nomination.tracer:
                self.nomination.tracer.event("landmark_discovery", self.report)
        return self.annotate(observations)

    def annotate(self, places):
        """Reconcile again after source expansion; never preserve a now-ambiguous identity."""
        resolutions = self.resolutions(places)
        self.report.update(
            resolved=sum(r.resolved_place_id is not None for r in resolutions),
            unresolved=sum(r.resolved_place_id is None for r in resolutions),
        )
        if self.report.get("status") != "interrupted":
            self.report["status"] = "completed" if self.report["resolved"] else "degraded"
        self.acquisition.landmark_diagnostics = dict(self.report)
        landmarks = {}
        for rank, resolution in enumerate(resolutions, 1):
            if resolution.resolved_place_id:
                landmarks.setdefault(
                    resolution.resolved_place_id,
                    LandmarkIdentity(name=self.nomination.names[rank - 1], rank=rank),
                )
        return [
            p.model_copy(update={"landmark_nomination": landmarks.get(p.candidate.place_id)})
            for p in places
        ]
