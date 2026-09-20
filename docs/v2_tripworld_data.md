# TripWorld data and corpus construction

## Pinned metadata and preprocessing

Only CRUISEResearchGroup/TripWorld metadata/metadata_all.parquet is ingested.
Revision 421bc1dc63068bb398055b1ce987265fe22415db; SHA-256
bd94d73c8443a18b5c7d31c0bd0b855cd141763b63841ee90646be1d73f9345e.
The checked manifest specifies 155,531,767 bytes and 687,173 source rows; these are recorded
artifact identifiers, not new profiling in this documentation task.

The eleven fields are fsq_place_id, fsq_name, fsq_latitude, fsq_longitude, fsq_locality, fsq_region,
fsq_country, fsq_category_labels, google_name, google_categories and google_place_id. No reviews,
travel_behaviors or place_attributes are required. Validate schema/checksum/revision and build
deterministic repeatable artifacts. Code/manifests/tiny fixtures are versioned; raw/projected and
generated outputs are ignored. tools/data/prepare_tripworld.py wraps backend/app/tripworld preparation.

## Profiling and geographic method

Profile row counts, name/Google-ID/coordinate coverage, geography forms, category distributions,
duplicate identities and non-travel categories. Use coordinates rather than locality==city, so
suburbs are not discarded. Geographic search uses bounding box then Haversine circle, retaining
missing country and rejecting known contradictions when country is supplied; invalid coordinates
are excluded. Dateline, poles and circle boundaries remain explicit. Actual coverage counts,
sampling conditions and identity anomalies are preserved in v2_development, not recomputed here.

## Retrieval entities and text

Group by nonblank Google Place ID, otherwise FSQ ID. Source identity does not mean current Google
verification. Preferred names use normalized Google-name frequency then FSQ names with stable
ties/aliases/categories. Unicode/case normalization removes duplicated aliases/categories. Use
an observed coordinate medoid, not an invented average; preserve constituent FSQ IDs, geographic
values and spread/country-conflict flags. Different IDs may still represent one real place.

Documents contain names/alternative names, locality/region/country and categories. IDs and
latitude/longitude remain metadata, not embedding text. RAW/ENRICHED entity texts are deterministic;
versioned category enrichment adds retrieval meaning, not experience/official facts. Null handling
must not invent descriptions. The exact template/policy remains in corpus/entity builders and
versioned data/tripworld manifests. retrieval_entities.parquet, tripworld-retrieval-entity-v1 and
tripworld-entity-text-v1 identify the established entity layer. Its original hashes/counts and
earlier observed anomalies remain in [V2 development](v2_development.md).

## Artifact integrity and text layers

Projected Arrow schema follows manifest logical types. Corpus enrichment retains all selected
source rows and appends normalized FSQ/Google categories, semantic rule IDs, direct/inferred semantics,
eligibility hints, retrieval_description and retrieval_text. Production filtering happens later,
not by silently deleting source rows during enrichment. Fingerprints include selected artifact SHA,
schema/artifact/mapping/description/template versions, mapping payload and Parquet writer settings.
A compatible artifact plus matching manifest can be reused; writes use a temporary .part then atomic
replacement, followed by output SHA/size/count metadata. Current writer uses Parquet2.6, zstd and
dictionary encoding. This repeatability contract does not imply provider/API regeneration is bit-identical.

## Null, category and entity-text formatting

clean_text applies NFKC and whitespace collapse; null/blank values remain absent. FSQ category
paths retain nonempty hierarchy segments separated by ` > `. Non-list category input produces
an empty collection. Google categories also expand valid JSON-list strings, replace underscores
with spaces, and casefold-deduplicate normalized values. No textual null placeholder is invented.

The entity-level RAW text emits only populated lines in this order: Name, Aliases, Localities,
Regions, Countries, FSQ categories, Google categories. Multi-values use stable semicolon-separated
unions. ENRICHED appends Description only when one exists. This entity template differs from the
earlier row-level Name/Alternative name/Location/Categories/Description formatting; they are
successive corpus layers, not two competing runtime templates. IDs and coordinates remain metadata.
