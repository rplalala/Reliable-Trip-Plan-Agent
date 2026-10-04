# Keep independent evaluation outside the planner

Status: Accepted existing module boundary; Tickets 01-12 have approved offline implementations.

Using a planner's own validator or cached claims as factual ground truth would couple the
assessment to the mechanism under study. The evaluator instead reads a user-selected,
source-linked batch and independently applicable evidence, preserving UNKNOWN and explicit
availability. Final-quality scoring reads saved outputs. The isolated controlled-replay
executor reuses the actual V3 post-primary path with frozen offline capabilities and
separately reviewed outcomes; it does not run full planners or generate formal cases.
This costs additional evidence
and adjudication work but avoids treating internal success as independent correctness.
See [evaluation architecture](../0006-independent-evaluation.md) for delivered boundaries.
Formal collection, case construction, comparative analysis and research conclusions
remain separately authorized.
