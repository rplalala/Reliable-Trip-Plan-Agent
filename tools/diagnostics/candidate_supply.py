"""Read saved captures only; no network, SQL, model, or production writes."""

import argparse
import asyncio
import hashlib
import json
from datetime import date
from pathlib import Path
from uuid import uuid4

from backend.app.evidence.models import PlaceCandidate
from backend.app.evidence.selection_models import PlaceSelectionInput
from backend.app.evidence.selection_normalization import normalize_place_details_for_selection
from backend.app.integrations.google.places import GooglePlacesProvider
from backend.app.integrations.models import LatLng, PlaceDetailsRequest, RouteWaypoint
from backend.app.llm.azure_foundry.dto import FoundryPrimaryItineraryDTO
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.poi_selection import evaluate_poi_eligibility
from backend.app.policies.route_matrix_chunking import partition_baseline_origins
from backend.app.runtime.token_counting import count_tokens


class SavedTransport:
    def __init__(self, payload):
        self.payload = payload

    async def request_json(self, *args, **kwargs):
        return self.payload


async def analyze(root, output, trip_end, generation_capture):
    live = json.loads((root / "live_result.json").read_text(encoding="utf-8"))
    trace = Path(live["trace_directory"])
    events = [
        json.loads(s) for s in (trace / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    admission = next(e["payload"] for e in events if e["event"] == "semantic_candidate_admission")
    supply = next(e["payload"] for e in events if e["event"] == "planning_supply_completed")
    ordered = admission["admitted_ids"] + admission["omitted_ids"]
    origins = live["result"]["rag_discovery"]["origins"]
    details = {}
    hashes = {}
    for path in sorted((trace / "tools").glob("*_google_places_details.json")):
        raw = path.read_bytes()
        item = json.loads(raw)
        details[item["request"]["place_id"]] = item
        hashes[str(path)] = hashlib.sha256(raw).hexdigest()
    rows = []
    for pid, links in origins.items():
        capture = details[pid]
        provider = GooglePlacesProvider(
            api_key="offline-placeholder",
            transport=SavedTransport(capture["response"]),
            tracer=NullRunTracer(uuid4()),
        )
        dto = await provider.get_place_details(
            PlaceDetailsRequest(
                place_id=pid, field_mask=capture["request"]["headers"]["X-Goog-FieldMask"]
            )
        )
        cheap = PlaceSelectionInput(
            candidate=PlaceCandidate(
                place_id=pid,
                name=dto.display_name,
                latitude=dto.location.latitude,
                longitude=dto.location.longitude,
                primary_type=dto.primary_type,
                business_status=dto.business_status,
                source_query=links[0]["query"]["text"],
                category=links[0]["query"]["query_id"],
                provider_rank=None,
            ),
            discovery_origins=links,
        )
        normalized = normalize_place_details_for_selection(cheap, dto)
        gate = evaluate_poi_eligibility(normalized, trip_end=trip_end)
        rows.append(
            {
                "id": pid,
                "name": dto.display_name,
                "old_order_position": ordered.index(pid) + 1,
                "old_admitted": pid in admission["admitted_ids"],
                "old_enriched": pid in supply["details_attempts"],
                "old_supplied": pid in supply["selected_ids"],
                "saved_details_pass_common_gate": gate.eligible,
                "gate_reason": gate.reason,
                "mask": capture["request"]["headers"]["X-Goog-FieldMask"],
                "language": capture["request"]["params"]["languageCode"],
            }
        )
    formulas = []
    for days in range(1, 11):
        k = min(16, max(8, 2 * days + 6))
        g = 2 * k
        formulas.append(
            {
                "days": days,
                "C": max(48, 4 * k),
                "G": g,
                "K": k,
                "main_sends": g + 8,
                "P": min(8, (k + 1) // 2),
                "v2_details_send_upper": g + 8 + 20,
            }
        )
    routing = []
    for k in (8, 10, 12, 14, 16):
        points = [
            RouteWaypoint(place_id=f"synthetic_{i}", location=LatLng(latitude=0, longitude=0))
            for i in range(k)
        ]
        blocks = partition_baseline_origins(points, per_request_element_limit=64)
        pairs = [(p.place_id, q.place_id) for b in blocks for p in b for q in points]
        routing.append(
            {
                "K": k,
                "blocks": [len(b) * k for b in blocks],
                "total": len(pairs),
                "unique": len(set(pairs)),
            }
        )
    payload = json.loads(
        generation_capture.read_text(encoding="utf-8")
    )
    prompt_tokens = count_tokens(payload["system_prompt"]) + count_tokens(payload["user_prompt"])
    schema_tokens = count_tokens(
        json.dumps(FoundryPrimaryItineraryDTO.model_json_schema(), ensure_ascii=True)
    )
    result = {
        "analysis_scope": "saved observation only; not an expanded run or quality comparison",
        "observed_union": len(ordered),
        "observed_unique_details": len(details),
        "unobserved_details_in_fixed_union": len(set(ordered) - set(details)),
        "rag_rows": rows,
        "formulas": formulas,
        "routes": routing,
        "payload": {
            "actual_supply_count": len(supply["selected_ids"]),
            "engineering_prompt_tokens": prompt_tokens,
            "engineering_schema_tokens": schema_tokens,
            "engineering_combined": prompt_tokens + schema_tokens,
            "actual_provider_input_tokens": None,
            "actual_output_tokens": None,
            "K12_K16_actual_payload_available": False,
            "deployment_context_limit_verified": False,
        },
        "input_hashes": hashes,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "analysis.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {k: v for k, v in result.items() if k != "input_hashes"}, indent=2, ensure_ascii=True
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-root", type=Path, required=True)
    parser.add_argument("--generation-capture", type=Path, required=True)
    parser.add_argument("--trip-end", type=date.fromisoformat, required=True)
    parser.add_argument(
        "--output", type=Path, default=Path("artifacts/diagnostics/candidate_supply")
    )
    args = parser.parse_args()
    asyncio.run(analyze(args.capture_root, args.output, args.trip_end, args.generation_capture))


if __name__ == "__main__":
    main()
