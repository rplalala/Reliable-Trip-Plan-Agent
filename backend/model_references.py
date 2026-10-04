"""Deterministic request-local references for explicit structured identity fields."""

import hashlib
import json
from copy import deepcopy

VERSION = "model_short_references_1"
INSTRUCTION = (
    "Identity fields contain request-local short references, not external IDs. "
    "Return only supplied references in linked identity fields; never reconstruct long IDs. "
    "References are unrelated to rank or response order. The application restores canonical IDs."
)


class ShortReferences:
    """Map only declared fields/identity-keyed dictionaries, never arbitrary prose."""

    def __init__(self, payload, fields, *, keyed=None):
        self.fields = dict(fields)
        self.keyed = dict(keyed or {})
        pools = {prefix: set() for prefix in (*self.fields.values(), *self.keyed.values())}

        def collect(value, prefix=None):
            if isinstance(value, str) and prefix is not None:
                pools[prefix].add(value)
            elif isinstance(value, list):
                for item in value:
                    collect(item, prefix)
            elif isinstance(value, dict):
                for key, item in value.items():
                    if key in self.keyed:
                        pools[self.keyed[key]].update(item)
                        if key in self.fields:
                            for row in item.values():
                                collect(row, self.fields[key])
                    collect(item, self.fields.get(key))

        collect(payload)
        self.reverse = {
            prefix: {f"{prefix}{i:02d}": identifier for i, identifier in enumerate(sorted(ids), 1)}
            for prefix, ids in pools.items()
        }
        self.forward = {
            prefix: {identifier: ref for ref, identifier in rows.items()}
            for prefix, rows in self.reverse.items()
        }

    @property
    def manifest(self):
        return {
            "version": VERSION,
            "references": deepcopy(self.reverse),
            "fields": dict(self.fields),
            "keyed": dict(self.keyed),
        }

    @property
    def sha256(self):
        return hashlib.sha256(json.dumps(self.manifest, sort_keys=True).encode()).hexdigest()

    def _convert(self, value, mappings, *, field=None):
        if isinstance(value, str) and field in self.fields:
            try:
                return mappings[self.fields[field]][value]
            except KeyError as exc:
                raise ValueError("Unknown model reference in " + field) from exc
        if isinstance(value, list):
            return [self._convert(item, mappings, field=field) for item in value]
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if key in self.keyed:
                    result[key] = {
                        mappings[self.keyed[key]][identifier]: self._convert(
                            row, mappings, field=key
                        )
                        for identifier, row in item.items()
                    }
                else:
                    result[key] = self._convert(item, mappings, field=key)
            return result
        return value

    def encode(self, payload):
        return self._convert(payload, self.forward)

    def decode(self, payload):
        return self._convert(payload, self.reverse)

    def constrain_schema(self, schema):
        """Constrain linked fields, retaining existing nullability and schema shape."""
        schema = deepcopy(schema)

        def visit(value):
            if isinstance(value, list):
                for item in value:
                    visit(item)
            elif isinstance(value, dict):
                for field, node in value.get("properties", {}).items():
                    if field not in self.fields:
                        continue
                    choices = list(self.reverse[self.fields[field]])
                    target = node.get("items", node)
                    nullable = "null" in target.get("type", []) or any(
                        branch.get("type") == "null" for branch in target.get("anyOf", [])
                    )
                    if choices or nullable:
                        target["enum"] = choices + ([None] if nullable else [])
                for item in value.values():
                    visit(item)

        visit(schema)
        return schema
