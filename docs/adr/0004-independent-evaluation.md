# Keep independent evaluation outside the planner

Status: Accepted existing module boundary; partially implemented by Tickets 01-09.

Using a planner's own validator or cached claims as factual ground truth would couple the
assessment to the mechanism under study. The evaluator instead reads a user-selected,
source-linked batch and independently applicable evidence, preserving UNKNOWN and explicit
availability. It does not generate cases or execute planners. This costs additional evidence
and adjudication work but avoids treating internal success as independent correctness.
See [evaluation architecture](../0006-independent-evaluation.md); later planned reports
remain unimplemented until separately approved.
