"""Bounded output-claim syntax, without general title interpretation."""

import re
import unicodedata

from .records import text


def normalized(value):
    return " ".join(unicodedata.normalize("NFC", value).casefold().split()) if text(value) else None


def directed_claim(value):
    """Read a complete 'MODE from NAME to NAME' clause; names are not inferred."""
    value = normalized(value)
    if value is None:
        return None
    clause = value.split(";", 1)[0].removesuffix(".")
    match = re.fullmatch(
        r"(?:(?:walk|walking|drive|driving|transit|public transit|transfer|travel) )?"
        r"from (.+) to (.+)",
        clause,
    )
    return match.groups() if match else None


def movement_claim(value):
    value = normalized(value) or ""
    pair = directed_claim(value)
    if pair:
        return {"kind": "movement", "origin": pair[0], "destination": pair[1]}
    match = re.fullmatch(
        r"(?:walk|walking|drive|driving|transit|public transit|transfer|travel) to (.+)", value
    )
    return {"kind": "movement", "destination": match[1]} if match else None


def competing_title(value, place_name):
    """Recognize complete explicit visit/list/movement claims, not narrative meaning."""
    title, name = normalized(value), normalized(place_name)
    if not title or not name or title == name:
        return None
    movement = movement_claim(title)
    if movement:
        return movement
    if title.startswith("visit ") and title[6:] != name:
        return {"kind": "visit", "destination": title[6:]}
    if title.startswith(name + " and "):
        return {"kind": "additional_place", "destination": title[len(name) + 5 :]}
    return None


def claim_evidence(value, parsed, source):
    return {"source": source, "field": "title", "original": value, "parsed": parsed}


def transport_endpoints(raw):
    """Read supported endpoint declarations; unrelated prose supplies no endpoint claim."""
    pairs = []
    for field in ("title", "notes"):
        value = normalized(raw.get(field)) or ""
        for clause in value.split(";"):
            pair = directed_claim(clause)
            if pair is not None:
                pairs.append(pair)
    return {
        "declared": bool(pairs),
        "pair": pairs[0] if pairs and len(set(pairs)) == 1 else None,
    }
