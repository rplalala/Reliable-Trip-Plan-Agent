CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE tripworld.corpus_builds (
    artifact_hash text PRIMARY KEY,
    manifest jsonb NOT NULL,
    row_count bigint NOT NULL,
    ingested_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE tripworld.entities (
    retrieval_entity_id text PRIMARY KEY,
    google_place_id text,
    preferred_name text,
    normalized_names text[] NOT NULL,
    latitude double precision CHECK (latitude BETWEEN -90 AND 90),
    longitude double precision CHECK (longitude BETWEEN -180 AND 180),
    country text,
    eligibility_hint text NOT NULL CHECK (eligibility_hint IN ('eligible','ineligible','unknown')),
    exclusion_reasons text[] NOT NULL,
    policy_version text NOT NULL,
    discovery_allowed boolean NOT NULL,
    retrieval_text text NOT NULL,
    text_hash text NOT NULL,
    content_hash text NOT NULL,
    artifact_hash text NOT NULL REFERENCES tripworld.corpus_builds,
    metadata jsonb NOT NULL,
    CHECK (discovery_allowed = (cardinality(exclusion_reasons) = 0))
);
CREATE UNIQUE INDEX entities_google_id ON tripworld.entities(google_place_id)
    WHERE google_place_id IS NOT NULL;
CREATE INDEX entities_latitude ON tripworld.entities(latitude);
CREATE INDEX entities_longitude ON tripworld.entities(longitude);
CREATE INDEX entities_country ON tripworld.entities(country);
CREATE INDEX entities_names ON tripworld.entities USING gin(normalized_names);
CREATE INDEX entities_discovery_text ON tripworld.entities(text_hash) WHERE discovery_allowed;
CREATE TABLE tripworld.embedding_spaces (
    space_id text PRIMARY KEY,
    configuration jsonb NOT NULL
);
-- Content-addressed vectors can serve multiple entities with identical text.
-- Entity identity remains separate and determines retrieval slots.
CREATE TABLE tripworld.embeddings (
    space_id text NOT NULL REFERENCES tripworld.embedding_spaces,
    text_hash text NOT NULL,
    embedding vector(1536) NOT NULL,
    vector_hash text NOT NULL,
    generation_metadata jsonb NOT NULL,
    generated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (space_id, text_hash)
);
CREATE VIEW tripworld.entity_embeddings AS
SELECT e.retrieval_entity_id, e.content_hash, e.text_hash,
       v.space_id, v.embedding, v.generated_at
FROM tripworld.entities e JOIN tripworld.embeddings v USING (text_hash)
WHERE e.discovery_allowed;
