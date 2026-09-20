"""Shared first-draft objectives, not validators or repair instructions."""

FIRST_GENERATION_POLICY = """
Cover the entire requested date range. For a normal full trip day, normally target
2-5 distinct main POIs. This is a default generation target, not an unconditional
quota or a hard user requirement. Do not intentionally concentrate all visits in
early days and leave later dates empty. Respect explicit slow pace, rest preferences,
long-duration REQUIRED visits, evidence availability and supported date boundaries.
Do not invent places or facts to meet the target. Do not inflate counts with repeat
visits, transport, free time, generic activities or unscheduled Nearby references.
Provide activity_kind explicitly for every activity: main_poi for a primary venue
visit, generic_activity for a non-specific activity, transport for a transfer,
free_time for unallocated/rest time, or unknown when the role cannot be assigned.
These are model-declared roles, not evidence-backed factual verification. Place type
alone does not determine role. A REQUIRED cafe can be a main visit. Keep a coherent
draft and state material limitations when the target cannot reasonably be met;
do not fabricate supporting evidence or claim guaranteed daily feasibility.
""".strip()
