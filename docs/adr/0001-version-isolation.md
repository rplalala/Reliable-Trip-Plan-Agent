# Preserve independent versions in a modular monolith

Status: Accepted existing decision; recorded 2026-10-03, not newly introduced.

V0-V3 represent distinct mechanisms but share ordinary correctness and application
infrastructure. Keep separate runners/graphs/configuration inside one modular monolith
rather than overwriting earlier versions or operating four divergent services. This
preserves independently runnable paths without duplicating provider and schema maintenance.
Shared changes still require affected-version validation and cannot be described as a
later version's exclusive benefit. See [architecture](../0001-system-architecture.md).
