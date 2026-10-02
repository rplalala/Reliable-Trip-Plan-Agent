# Assign tool-version transport to the application

Status: Accepted and implemented existing decision; recorded 2026-10-03.

Mixing model transport activities with application transfers creates competing occupancy
and evidence claims. V1-V3 therefore forbid declared model transport and bind application
transfers to applicable route evidence; V0 retains clearly estimated model transport to
preserve its plain-LLM mechanism. Invalid declared transport fails acceptance rather than
being silently removed. This improves provenance consistency, without claiming complete
detection of transport disguised in prose. See [output contract](../0003-itinerary-transport.md).
