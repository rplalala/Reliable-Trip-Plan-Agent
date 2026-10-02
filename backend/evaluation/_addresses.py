"""Typed independent address comparisons with strict legacy fallback."""

import re

from ._claims import normalized
from .records import text


def components(candidate):
    raw = candidate.get("address_components")
    if "address_components" not in candidate:
        return {}
    if not isinstance(raw, list):
        raise ValueError("Address components must be an array")
    result = {}
    for item in raw:
        if not isinstance(item, dict) or not text(item.get("longText")):
            raise ValueError("Address component requires longText")
        kinds = item.get("types")
        if not isinstance(kinds, list) or not kinds or not all(text(k) for k in kinds):
            raise ValueError("Address component requires types")
        values = {normalized(item["longText"])}
        if "shortText" in item:
            if not text(item["shortText"]):
                raise ValueError("Invalid shortText")
            values.add(normalized(item["shortText"]))
        for kind in kinds:
            if kind == "political":
                continue
            if kind in result and result[kind] != values:
                raise ValueError("Conflicting address components")
            result[kind] = values
    return result


def legacy_match(value, candidate):
    target = normalized(value)
    return target is not None and target in {
        normalized(piece) for piece in re.split(r"[,;]", candidate["formatted_address"])
    }


def destination_matches(value, candidate):
    typed = components(candidate)
    if "locality" not in typed:
        return legacy_match(value, candidate)
    parts = [normalized(p) for p in re.split(r"[,;]", value)]
    qualifiers = set().union(
        *(
            typed.get(k, set())
            for k in ("country", "administrative_area_level_1", "administrative_area_level_2")
        )
    )
    return parts[0] in typed["locality"] and all(p in qualifiers for p in parts[1:])


def street_forms(typed):
    return {
        f"{number} {route}"
        for number in typed.get("street_number", ())
        for route in typed.get("route", ())
    }


def location_matches(value, candidate):
    typed = components(candidate)
    target = normalized(value)
    if numbered_street(value) and street_forms(typed):
        return target in street_forms(typed)
    if target in street_forms(typed) or any(target in values for values in typed.values()):
        return True
    if "locality" in typed:
        # Typed city evidence cannot be overridden by an untyped address token.
        return False
    return legacy_match(value, candidate)


def numbered_street(value):
    return bool(
        re.fullmatch(
            r"\d+[a-z]?(?:[-/]\d+[a-z]?)?\s+.+\s+"
            r"(?:street|st|road|rd|avenue|ave|lane|ln|drive|dr|boulevard|blvd|way|court|ct)\.?",
            normalized(value) or "",
        )
    )


def addresses_agree(left, right):
    a, b = components(left), components(right)
    if any(not a[k] & b[k] for k in a.keys() & b.keys()):
        return False
    if normalized(left["formatted_address"]) == normalized(right["formatted_address"]):
        return True
    required = {"street_number", "route", "locality", "country"}
    return required <= a.keys() and a.keys() == b.keys() and all(a[k] & b[k] for k in a)
