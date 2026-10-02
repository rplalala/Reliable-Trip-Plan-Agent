# Reuse one compatible persistent exact retrieval space

Status: Accepted and implemented existing decision; recorded 2026-10-03.

V2/V3 reuse the established PostgreSQL/pgvector corpus and geographic-filtered exact ranking.
Corpus construction is offline and runtime embeds queries only. Introducing an ANN index,
shadow table or a new vector space would alter compatibility and reproducibility assumptions;
none is an incidental optimization in the current design. Performance variation remains a
measured engineering limitation, not evidence that an unimplemented index exists. See
[retrieval design](../0004-retrieval-persistence%28v2v3%29.md).
