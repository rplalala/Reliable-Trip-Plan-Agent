"""Dated official retail references for observed events, never account invoices."""

from datetime import date, timedelta
from decimal import Decimal

CHECKED_ON = "2026-10-08"
GOOGLE_SOURCE = "https://developers.google.com/maps/billing-and-pricing/pricing"
MODEL_SOURCE = "https://developers.openai.com/api/docs/models/gpt-6-luna"
LUNA_RATES = {
    "input_tokens": "0.10",
    "cached_input_tokens": "0.01",
    "cache_write_input_tokens": "0.125",
    "output_tokens": "0.50",
}
LONG_CONTEXT_THRESHOLD = 272000
LONG_INPUT_MULTIPLIER = "2"
LONG_OUTPUT_MULTIPLIER = "1.5"
EMBEDDING_RATE = "0.020"
GOOGLE_RATES = {
    "text_search_ids_only": "0",
    "text_search_pro": "0.032",
    "nearby_pro": "0.032",
    "details_ids_only": "0",
    "details_essentials": "0.005",
    "details_pro": "0.017",
    "details_enterprise": "0.020",
    "details_reviews": "0.025",
}
MATRIX_RATES = {"essentials": "0.005", "pro": "0.010"}
WEB_SEARCH_RATE = "0.010"
DETAILS_IDS = {"id", "name", "attributions"}
DETAILS_ESSENTIALS = {"addressComponents", "formattedAddress", "location", "types"}
DETAILS_PRO = {
    "accessibilityOptions",
    "businessStatus",
    "displayName",
    "openingDate",
    "primaryType",
    "timeZone",
}
DETAILS_ENTERPRISE = {
    "currentOpeningHours",
    "regularOpeningHours",
    "rating",
    "websiteUri",
    "priceLevel",
    "priceRange",
}
SEARCH_PRO = DETAILS_IDS | DETAILS_ESSENTIALS | DETAILS_PRO


def reference_basis():
    return {
        "checked_on": CHECKED_ON,
        "currency": "USD",
        "actual_account_prices": False,
        "model": {
            "gpt-6-luna": {
                "input_per_million": LUNA_RATES["input_tokens"],
                "cached_input_per_million": LUNA_RATES["cached_input_tokens"],
                "cache_write_per_million": LUNA_RATES["cache_write_input_tokens"],
                "output_per_million": LUNA_RATES["output_tokens"],
                "long_context_threshold": LONG_CONTEXT_THRESHOLD,
                "long_input_multiplier": LONG_INPUT_MULTIPLIER,
                "long_output_multiplier": LONG_OUTPUT_MULTIPLIER,
                "source": MODEL_SOURCE,
            }
        },
        "embedding": {
            "model": "text-embedding-3-small",
            "input_per_million": EMBEDDING_RATE,
            "source": "https://developers.openai.com/api/docs/models/text-embedding-3-small",
        },
        "google_per_request": dict(GOOGLE_RATES),
        "matrix_per_element": dict(MATRIX_RATES),
        "web_search_per_tool_call": WEB_SEARCH_RATE,
        "google_source": GOOGLE_SOURCE,
        "tool_source": "https://developers.openai.com/api/docs/pricing",
        "assumptions": [
            "Standard processing; no account discounts, free quotas or tax.",
            "OpenAI model/tool rates proxy Foundry rates; actual account billing unavailable.",
            "Missing cache details use an explicit conservative estimate, never observed zero.",
            "Open-Meteo noncommercial endpoint and public HTML have no per-request fee "
            "in this scenario.",
            "Failed requests and missing provider usage remain unpriced; no invoice is inferred.",
        ],
    }


def _provider_price(event):
    provider, operation = event["provider"], event["operation"]
    context = event.get("billing_context", {})
    if provider == "azure_foundry" and operation == "web_search_tool":
        return (
            {"tool_calls": WEB_SEARCH_RATE},
            "https://developers.openai.com/api/docs/pricing",
            "Web Search tool",
        )
    if (provider, operation) in (("open_meteo", "weather"), ("official_website", "page_http")):
        return (
            {"requests": "0"},
            "https://open-meteo.com/en/pricing" if provider == "open_meteo" else "public-html",
            "Free-use reference scenario",
        )
    if provider != "google":
        return None
    if operation == "route_matrix":
        mode, preference = context.get("travel_mode"), context.get("routing_preference")
        if mode not in ("WALK", "TRANSIT", "DRIVE") or preference not in (
            None,
            "TRAFFIC_UNAWARE",
            "TRAFFIC_AWARE",
            "TRAFFIC_AWARE_OPTIMAL",
        ):
            return None
        pro = preference in ("TRAFFIC_AWARE", "TRAFFIC_AWARE_OPTIMAL")
        return (
            {"element_count": MATRIX_RATES["pro" if pro else "essentials"]},
            GOOGLE_SOURCE,
            "Matrix Pro" if pro else "Matrix Essentials",
        )
    mask = context.get("field_mask", "")
    if not mask:
        return None
    fields = {field.removeprefix("places.").split(".")[0] for field in mask.split(",")}
    fields.discard("nextPageToken")
    endpoint = context.get("endpoint")
    if operation == "places_search" and endpoint in ("searchText", "searchNearby"):
        if not fields or not fields <= SEARCH_PRO:
            return None
        if endpoint == "searchText" and fields <= DETAILS_IDS:
            return (
                {"requests": GOOGLE_RATES["text_search_ids_only"]},
                GOOGLE_SOURCE,
                "Text Search IDs Only",
            )
        # Current planners/identity search request Pro fields; no unseen masks are inferred.
        return (
            {
                "requests": GOOGLE_RATES[
                    "text_search_pro" if endpoint == "searchText" else "nearby_pro"
                ]
            },
            GOOGLE_SOURCE,
            "Text Search Pro" if endpoint == "searchText" else "Nearby Search Pro",
        )
    if operation == "place_details" and endpoint == "details":
        if (
            not fields
            or not fields
            <= DETAILS_IDS | DETAILS_ESSENTIALS | DETAILS_PRO | DETAILS_ENTERPRISE | {"reviews"}
        ):
            return None
        sku, rate = (
            ("Details Enterprise + Atmosphere", GOOGLE_RATES["details_reviews"])
            if "reviews" in fields
            else ("Details Enterprise", GOOGLE_RATES["details_enterprise"])
            if fields & DETAILS_ENTERPRISE
            else ("Details Pro", GOOGLE_RATES["details_pro"])
            if fields & DETAILS_PRO
            else ("Details Essentials", GOOGLE_RATES["details_essentials"])
            if fields & DETAILS_ESSENTIALS
            else ("Details IDs Only", GOOGLE_RATES["details_ids_only"])
        )
        return {"requests": rate}, GOOGLE_SOURCE, sku
    return None


def build_reference_prices(sources):
    """Bind explicit price rows to saved event identities and observed request context."""
    rows, excluded = [], []
    for source in sources:
        usage = source["usage"]
        observed = date.fromisoformat(usage["timing"]["started_at"][:10])
        for kind, field in (("model", "model_calls"), ("provider", "provider_events")):
            for event in usage[field]:
                match = {
                    "kind": kind,
                    **{k: event[k] for k in ("provider", "operation", "event_id")},
                }
                extra = {}
                if kind == "model":
                    match["model"] = event.get("model")
                    if (
                        event.get("model") == "text-embedding-3-small"
                        and event["operation"] == "embedding"
                    ):
                        rates, url, sku = (
                            {"input_tokens": EMBEDDING_RATE},
                            reference_basis()["embedding"]["source"],
                            "Query embedding",
                        )
                    elif event.get("model") == "gpt-6-luna":
                        long = (
                            type(event.get("input_tokens")) is int
                            and event["input_tokens"] > LONG_CONTEXT_THRESHOLD
                        )
                        rates = dict(LUNA_RATES)
                        if long:
                            input_multiplier = Decimal(LONG_INPUT_MULTIPLIER)
                            output_multiplier = Decimal(LONG_OUTPUT_MULTIPLIER)
                            rates = {
                                unit: str(
                                    Decimal(rate)
                                    * (
                                        output_multiplier
                                        if unit == "output_tokens"
                                        else input_multiplier
                                    )
                                )
                                for unit, rate in rates.items()
                            }
                        url, sku = (
                            MODEL_SOURCE,
                            "GPT-6 Luna long context" if long else "GPT-6 Luna short context",
                        )
                        extra["unreported_cache_policy"] = "uncached_write_rate"
                    else:
                        excluded.append(
                            {"event_id": event["event_id"], "reason": "unknown_model_reference"}
                        )
                        continue
                    per = "1000000"
                else:
                    resolved = _provider_price(event)
                    if resolved is None:
                        # Model HTTP is accounted through its model event, not another charge.
                        continue
                    rates, url, sku = resolved
                    per = "1"
                    if event.get("billing_context"):
                        match["billing_context"] = event["billing_context"]
                rows.append(
                    {
                        "price_id": source["sha256"] + ":" + kind + ":" + event["event_id"],
                        "source": url,
                        "as_of": CHECKED_ON,
                        "valid_from": str(observed),
                        "valid_until": str(observed + timedelta(days=1)),
                        "match": match,
                        "rates": rates,
                        "per": per,
                        "sku_reference": sku,
                        "assumption": (
                            "Dated official retail reference for saved usage; not an account "
                            "invoice. Standard processing; no tax, credits or free quota."
                        ),
                        **extra,
                    }
                )
    return {
        "schema_version": "rtpeval_prices_1",
        "currency": "USD",
        "rows": rows,
        "reference_basis": reference_basis(),
        "excluded_model_references": excluded,
    }
