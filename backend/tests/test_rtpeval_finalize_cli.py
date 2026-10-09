"""Synthetic external-agent material through the installed offline CLI boundary."""

import copy
import json

import pytest

from backend.tests import test_rtpeval_cli as cli_tests
from backend.tests import test_rtpeval_collect_cli as collect_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
installed_cli = cli_tests.installed_cli
collection = collect_tests.collection


def synthetic_execution(artifact, root, operation, record):
    """Construct new explicitly synthetic source-bound execution/transcript evidence."""
    execution = {
        key: copy.deepcopy(item) for key, item in record.items() if key != "transcript_ref"
    }
    transcript = {
        "schema_version": "rtpeval_requirement_agent_transcript_1",
        "synthetic_fixture": True,
        "execution": execution,
        "messages": [{"role": "assistant", "content": "Synthetic fixture; no agent was run."}],
    }
    record["transcript_ref"] = artifact(
        operation + "-transcript.json", transcript, transcript["schema_version"]
    )
    return artifact(operation + "-execution.json", record, record["schema_version"])


@pytest.fixture
def handoff(collection, batch):
    config, save, root = collection
    _, _, _, artifact, _ = batch
    group = config["groups"][0]
    spec = json.loads((root / "requirements.json").read_bytes())
    spec["review"] = {
        "status": "reviewed",
        "reviewer_ref": "synthetic-reviewer",
        "reviewed_at": "2026-10-09T01:03:00Z",
    }
    spec_ref = artifact("requirements.json", spec, "rtpeval_requirements_1")
    authored = copy.deepcopy(spec)
    authored["review"] = {"status": "pending"}
    draft_ref = artifact("authored-requirements.json", authored, authored["schema_version"])
    records = {}
    for operation, minute in (("authoring", "01"), ("review", "03")):
        record = {
            "schema_version": "rtpeval_requirement_agent_execution_1",
            "operation": operation,
            "origin": "external_codex",
            "actor_ref": "synthetic-author" if operation == "authoring" else "synthetic-reviewer",
            "execution_id": "synthetic-" + operation,
            "group_id": "g",
            "input_sha256": group["input_ref"]["sha256"],
            "requirement_spec_sha256": (draft_ref if operation == "authoring" else spec_ref)[
                "sha256"
            ],
            "started_at": "2026-10-09T01:" + minute + ":00Z",
            "completed_at": "2026-10-09T01:" + minute + ":00Z",
            "configuration": {"agent": "Codex", "model": "gpt-6.1-sol", "reasoning_effort": "high"},
            "context": {
                "source": "complete_original_request",
                "excluded": [
                    "planner_interpretation",
                    "generated_outputs",
                    "scores",
                    "mechanisms",
                ],
            },
            "source_input_ref": group["input_ref"],
            "requirement_spec_ref": draft_ref if operation == "authoring" else spec_ref,
        }
        if operation == "review":
            record["input_requirement_spec_ref"] = draft_ref
            record["input_requirement_spec_sha256"] = draft_ref["sha256"]
        records[operation + "_ref"] = synthetic_execution(artifact, root, operation, record)
    value = {
        "schema_version": "rtpeval_requirement_handoff_1",
        "batch_id": "batch",
        "groups": [
            {
                "group_id": "g",
                "input_ref": group["input_ref"],
                "requirement_spec_ref": spec_ref,
                "authored_requirement_spec_ref": draft_ref,
                **records,
            }
        ],
    }
    path = root / "handoff.json"

    def write():
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    return value, write, save, root


def test_reviewed_handoff_finalizes_native_batch_without_source_changes(installed_cli, handoff):
    _, write, save, root = handoff
    source, handoff_path = save(), write()
    originals = {p: p.read_bytes() for p in root.glob("*.json")}
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", source, "--directory", staging).returncode == 0
    result = installed_cli(
        "batch",
        "attach-requirements",
        staging / "staging.json",
        handoff_path,
        "--directory",
        attached,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (attached / "manifest.json").exists()
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "accepted"
    accepted = installed_cli("validate", final / "manifest.json")
    assert accepted.returncode == 0, accepted.stdout + accepted.stderr
    assert json.loads(accepted.stdout)["status"] == "accepted"
    stage = json.loads((staging / "staging.json").read_bytes())
    for ref in stage["artifact_bindings"]:
        assert (final / ref["path"]).read_bytes() == (staging / ref["path"]).read_bytes()
    assert {p: p.read_bytes() for p in originals} == originals


def test_external_configuration_can_retain_additional_actual_execution_options(
    installed_cli, handoff, batch
):
    value, write, save, root = handoff
    artifact = batch[3]
    for operation in ("authoring", "review"):
        ref = value["groups"][0][operation + "_ref"]
        record = json.loads((root / ref["path"]).read_bytes())
        record["configuration"]["session_mode"] = "separately-operated-offline-handoff"
        value["groups"][0][operation + "_ref"] = synthetic_execution(
            artifact, root, operation, record
        )
    staging = root / "staging"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    result = installed_cli(
        "batch",
        "attach-requirements",
        staging / "staging.json",
        write(),
        "--directory",
        root / "attached",
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "fault",
    [
        "reviewed_only",
        "human_relabel",
        "wrong_model",
        "wrong_effort",
        "missing_origin",
        "missing_time",
        "naive_time",
        "review_before_author",
        "shared_execution",
        "shared_actor",
        "planner_context",
        "source_binding",
        "spec_binding",
        "missing_source_ref",
        "missing_spec_ref",
        "missing_transcript",
        "transcript_drift",
        "empty_transcript",
        "unreviewed",
        "reviewer_mismatch",
        "review_time_mismatch",
        "invented_quote",
        "escaping_spec",
        "duplicate_group",
        "wrong_batch",
        "changed_input",
    ],
)
def test_attachment_rejects_unbound_or_unreviewed_external_evidence(
    installed_cli, handoff, batch, fault
):
    value, write, save, root = handoff
    artifact = batch[3]
    group = value["groups"][0]
    ref = group["review_ref"]
    record = json.loads((root / ref["path"]).read_bytes())
    if fault == "reviewed_only":
        group.pop("review_ref")
    elif fault == "human_relabel":
        record["origin"] = "human_review"
    elif fault in ("wrong_model", "wrong_effort"):
        record["configuration"]["model" if fault == "wrong_model" else "reasoning_effort"] = "wrong"
    elif fault in (
        "missing_origin",
        "missing_time",
        "missing_source_ref",
        "missing_spec_ref",
        "missing_transcript",
    ):
        record.pop(
            {
                "missing_origin": "origin",
                "missing_time": "completed_at",
                "missing_source_ref": "source_input_ref",
                "missing_spec_ref": "requirement_spec_ref",
                "missing_transcript": "transcript_ref",
            }[fault]
        )
    elif fault == "naive_time":
        record["started_at"] = "2026-10-09T01:03:00"
    elif fault == "review_before_author":
        record["started_at"] = "2026-10-09T00:00:00Z"
    elif fault in ("shared_execution", "shared_actor"):
        record["execution_id" if fault == "shared_execution" else "actor_ref"] = (
            "synthetic-authoring" if fault == "shared_execution" else "synthetic-author"
        )
    elif fault == "planner_context":
        record["context"]["source"] = "planner_interpretation"
    elif fault in ("source_binding", "spec_binding"):
        record["input_sha256" if fault == "source_binding" else "requirement_spec_sha256"] = (
            "0" * 64
        )
    elif fault in ("transcript_drift", "empty_transcript"):
        transcript = root / record["transcript_ref"]["path"]
        transcript.write_bytes(b"drift" if fault == "transcript_drift" else b"")
        if fault == "empty_transcript":
            import hashlib

            record["transcript_ref"]["sha256"] = hashlib.sha256(b"").hexdigest()
            record["transcript_ref"]["media_type"] = "text/plain"
    elif fault in ("unreviewed", "reviewer_mismatch", "review_time_mismatch", "invented_quote"):
        spec = json.loads((root / "requirements.json").read_bytes())
        if fault == "unreviewed":
            spec["review"]["status"] = "pending"
        elif fault == "reviewer_mismatch":
            spec["review"]["reviewer_ref"] = "someone-else"
        elif fault == "review_time_mismatch":
            spec["review"]["reviewed_at"] = "2026-10-09T01:04:00Z"
        else:
            spec["obligations"] = [
                {
                    "obligation_id": "x",
                    "kind": "protected_time",
                    "resolution": "unsupported",
                    "source_refs": [{"field_path": "additional_preferences", "quote": "invented"}],
                }
            ]
        group["requirement_spec_ref"] = artifact(
            "requirements.json", spec, "rtpeval_requirements_1"
        )
    elif fault == "escaping_spec":
        group["requirement_spec_ref"]["path"] = "../outside.json"
    elif fault == "duplicate_group":
        value["groups"].append(copy.deepcopy(group))
    elif fault == "wrong_batch":
        value["batch_id"] = "another-batch"
    if fault != "reviewed_only":
        group["review_ref"] = artifact(ref["path"], record, record["schema_version"])
    staging = root / "staging"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    if fault == "changed_input":
        (root / "input.json").write_bytes(b"{}")
    handoff_path = write()
    originals = {p: p.read_bytes() for p in root.glob("*.json")}
    attached = root / "attached"
    result = installed_cli(
        "batch",
        "attach-requirements",
        staging / "staging.json",
        handoff_path,
        "--directory",
        attached,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "needs_material_correction"
    assert not attached.exists()
    assert {p: p.read_bytes() for p in originals} == originals


@pytest.mark.parametrize(
    "fault",
    [
        "missing_version",
        "invalid_completion",
        "missing_completion",
        "original_drift",
        "copied_drift",
        "stage_completion_edit",
        "attached_drift",
        "handoff_drift",
        "attachment_edit",
        "existing_destination",
    ],
)
def test_finalize_never_publishes_invalid_or_stale_material(installed_cli, handoff, fault):
    _, write, save, root = handoff
    # Alter the explicit producer configuration through its saved public wire.
    source = save()
    configuration = json.loads(source.read_bytes())
    if fault == "missing_version":
        del configuration["groups"][0]["selected_runs"]["v2"]
    elif fault in ("invalid_completion", "missing_completion"):
        run = configuration["groups"][0]["selected_runs"]["v3"]
        if fault == "missing_completion":
            run.pop("completion")
        else:
            run["completion"]["required_mechanisms"]["validation"] = "failed"
    if fault in ("missing_version", "invalid_completion", "missing_completion"):
        source.write_text(json.dumps(configuration), encoding="utf-8")
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", source, "--directory", staging).returncode == 0
    assert (
        installed_cli(
            "batch",
            "attach-requirements",
            staging / "staging.json",
            write(),
            "--directory",
            attached,
        ).returncode
        == 0
    )
    if fault == "original_drift":
        (root / "v0.json").write_bytes(b"{}")
    elif fault == "copied_drift":
        (staging / "sources/v0.json").write_bytes(b"{}")
    elif fault == "stage_completion_edit":
        stage = json.loads((staging / "staging.json").read_bytes())
        stage["groups"][0]["selected_runs"]["v0"]["completion"]["declared_by"] = "forged"
        (staging / "staging.json").write_text(json.dumps(stage), encoding="utf-8")
    elif fault == "attached_drift":
        (attached / "requirements/review-transcript.json").write_bytes(b"{}")
    elif fault == "handoff_drift":
        (root / "review-transcript.json").write_bytes(b"{}")
    elif fault == "attachment_edit":
        attachment = json.loads((attached / "attachment.json").read_bytes())
        attachment["groups"][0]["requirement_spec_ref"]["sha256"] = "0" * 64
        (attached / "attachment.json").write_text(json.dumps(attachment), encoding="utf-8")
    elif fault == "existing_destination":
        final.mkdir()
        (final / "manifest.json").write_bytes(b"original-finalized-manifest")
    originals = {p: p.read_bytes() for p in root.glob("*.json")}
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 2, result.stdout + result.stderr
    if fault == "existing_destination":
        assert (final / "manifest.json").read_bytes() == b"original-finalized-manifest"
    else:
        assert not (final / "manifest.json").exists()
    assert {p: p.read_bytes() for p in originals} == originals


def test_native_intake_is_required_before_final_manifest_publication(installed_cli, handoff, batch):
    value, write, save, root = handoff
    artifact = batch[3]
    source = save()
    configuration = json.loads(source.read_bytes())
    group = configuration["groups"][0]
    original = json.loads((root / "input.json").read_bytes())
    original["traveler_count"] = 0
    group["input_ref"] = artifact("input.json", original)
    for run in group["selected_runs"].values():
        ref = run["provenance_ref"]
        provenance = json.loads((root / ref["path"]).read_bytes())
        provenance["input_sha256"] = group["input_ref"]["sha256"]
        run["provenance_ref"] = artifact(ref["path"], provenance, provenance["schema_version"])
    handoff_group = value["groups"][0]
    handoff_group["input_ref"] = group["input_ref"]
    spec = json.loads((root / "requirements.json").read_bytes())
    spec["input_sha256"] = group["input_ref"]["sha256"]
    spec_ref = artifact("requirements.json", spec, spec["schema_version"])
    handoff_group["requirement_spec_ref"] = spec_ref
    authored = json.loads((root / "authored-requirements.json").read_bytes())
    authored["input_sha256"] = group["input_ref"]["sha256"]
    draft_ref = artifact("authored-requirements.json", authored, authored["schema_version"])
    handoff_group["authored_requirement_spec_ref"] = draft_ref
    for operation in ("authoring", "review"):
        ref = handoff_group[operation + "_ref"]
        record = json.loads((root / ref["path"]).read_bytes())
        record.update(
            input_sha256=group["input_ref"]["sha256"],
            requirement_spec_sha256=(draft_ref if operation == "authoring" else spec_ref)["sha256"],
            source_input_ref=group["input_ref"],
            requirement_spec_ref=draft_ref if operation == "authoring" else spec_ref,
        )
        if operation == "review":
            record["input_requirement_spec_ref"] = draft_ref
            record["input_requirement_spec_sha256"] = draft_ref["sha256"]
        handoff_group[operation + "_ref"] = synthetic_execution(artifact, root, operation, record)
    source.write_text(json.dumps(configuration), encoding="utf-8")
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", source, "--directory", staging).returncode == 0
    assert (
        installed_cli(
            "batch",
            "attach-requirements",
            staging / "staging.json",
            write(),
            "--directory",
            attached,
        ).returncode
        == 0
    )
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "Native intake rejected" in result.stdout
    assert "traveler" in result.stdout
    assert final.exists()
    assert not (final / "manifest.json").exists()
    assert not (final / "intake-candidate.json").exists()


def test_finalization_preserves_generation_and_review_sidecar_bytes(installed_cli, handoff, batch):
    import hashlib

    value, write, save, root = handoff
    artifact = batch[3]
    source = save()
    configuration = json.loads(source.read_bytes())
    binary = b"\x00\xffexact-original-sidecar"
    (root / "raw.bin").write_bytes(binary)
    evidence_ref = artifact(
        "evidence-index.json",
        {
            "schema_version": "rtpeval_generation_evidence_1",
            "artifacts": [{"path": "raw.bin", "sha256": hashlib.sha256(binary).hexdigest()}],
        },
        "rtpeval_generation_evidence_1",
    )
    run = configuration["groups"][0]["selected_runs"]["v0"]
    provenance = json.loads((root / run["provenance_ref"]["path"]).read_bytes())
    provenance["evidence_index_ref"] = evidence_ref
    run["provenance_ref"] = artifact("v0-provenance.json", provenance, provenance["schema_version"])
    transcript = json.loads((root / "review-transcript.json").read_bytes())
    transcript["retained_attachment"] = {
        "path": "raw.bin",
        "sha256": hashlib.sha256(binary).hexdigest(),
        "media_type": "application/octet-stream",
        "availability": "available",
    }
    transcript_ref = artifact("review-transcript.json", transcript, transcript["schema_version"])
    record = json.loads((root / "review-execution.json").read_bytes())
    record["transcript_ref"] = transcript_ref
    value["groups"][0]["review_ref"] = artifact(
        "review-execution.json", record, record["schema_version"]
    )
    source.write_text(json.dumps(configuration), encoding="utf-8")
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", source, "--directory", staging).returncode == 0
    assert (
        installed_cli(
            "batch",
            "attach-requirements",
            staging / "staging.json",
            write(),
            "--directory",
            attached,
        ).returncode
        == 0
    )
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (final / "sources/raw.bin").read_bytes() == binary
    assert (final / "requirements/raw.bin").read_bytes() == binary
    assert (final / "sources/evidence-index.json").read_bytes() == (
        root / "evidence-index.json"
    ).read_bytes()
    assert (final / "requirements/review-transcript.json").read_bytes() == (
        root / "review-transcript.json"
    ).read_bytes()
    assert installed_cli("validate", final / "manifest.json").returncode == 0


@pytest.mark.parametrize(
    "arguments",
    [
        ("batch", "attach-requirements", "--help"),
        ("batch", "finalize", "--help"),
    ],
)
def test_attachment_and_finalization_help_are_lazy_and_offline(installed_cli, arguments):
    result = installed_cli(*arguments, block_intake=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "offline" in result.stdout.lower()


def test_unchanged_transcript_cannot_be_rebound_by_editing_execution_hashes(
    installed_cli, handoff, batch
):
    value, write, save, root = handoff
    artifact = batch[3]
    group = value["groups"][0]
    # A new final spec requires new source-bound execution evidence; changing record hashes
    # while reusing the old transcript does not establish that the new artifact was reviewed.
    spec = json.loads((root / "requirements.json").read_bytes())
    spec["revision"] = "2"
    spec_ref = artifact("requirements-v2.json", spec, spec["schema_version"])
    group["requirement_spec_ref"] = spec_ref
    for operation in ("review",):
        ref = group[operation + "_ref"]
        record = json.loads((root / ref["path"]).read_bytes())
        record["requirement_spec_sha256"] = spec_ref["sha256"]
        record["requirement_spec_ref"] = spec_ref
        group[operation + "_ref"] = artifact(ref["path"], record, record["schema_version"])
    staging = root / "staging"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    result = installed_cli(
        "batch",
        "attach-requirements",
        staging / "staging.json",
        write(),
        "--directory",
        root / "attached",
    )
    assert result.returncode == 2, result.stdout + result.stderr
    assert "transcript" in result.stdout.lower()


def test_authored_draft_and_reviewed_final_keep_actual_artifact_lineage(
    installed_cli, handoff, batch
):
    value, write, save, root = handoff
    artifact = batch[3]
    group = value["groups"][0]
    authored = json.loads((root / "requirements.json").read_bytes())
    authored["review"] = {"status": "pending"}
    authored["revision"] = "author-draft"
    draft_ref = artifact("authored-requirements.json", authored, authored["schema_version"])
    group["authored_requirement_spec_ref"] = draft_ref
    author_ref = group["authoring_ref"]
    author = json.loads((root / author_ref["path"]).read_bytes())
    author.update(requirement_spec_sha256=draft_ref["sha256"], requirement_spec_ref=draft_ref)
    group["authoring_ref"] = synthetic_execution(artifact, root, "authoring", author)
    review_ref = group["review_ref"]
    review = json.loads((root / review_ref["path"]).read_bytes())
    review.update(
        input_requirement_spec_sha256=draft_ref["sha256"], input_requirement_spec_ref=draft_ref
    )
    group["review_ref"] = synthetic_execution(artifact, root, "review", review)
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    result = installed_cli(
        "batch", "attach-requirements", staging / "staging.json", write(), "--directory", attached
    )
    assert result.returncode == 0, result.stdout + result.stderr
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (final / "requirements/authored-requirements.json").read_bytes() == (
        root / "authored-requirements.json"
    ).read_bytes()
    assert (final / "requirements/requirements.json").read_bytes() == (
        root / "requirements.json"
    ).read_bytes()
    assert installed_cli("validate", final / "manifest.json").returncode == 0


def test_author_output_cannot_contain_future_review_metadata(installed_cli, handoff, batch):
    value, write, save, root = handoff
    artifact = batch[3]
    group = value["groups"][0]
    group["authored_requirement_spec_ref"] = group["requirement_spec_ref"]
    record = json.loads((root / "authoring-execution.json").read_bytes())
    record["requirement_spec_ref"] = group["requirement_spec_ref"]
    record["requirement_spec_sha256"] = group["requirement_spec_ref"]["sha256"]
    group["authoring_ref"] = synthetic_execution(artifact, root, "authoring", record)
    record = json.loads((root / "review-execution.json").read_bytes())
    record["input_requirement_spec_ref"] = group["requirement_spec_ref"]
    record["input_requirement_spec_sha256"] = group["requirement_spec_ref"]["sha256"]
    group["review_ref"] = synthetic_execution(artifact, root, "review", record)
    staging = root / "staging"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    result = installed_cli(
        "batch",
        "attach-requirements",
        staging / "staging.json",
        write(),
        "--directory",
        root / "attached",
    )
    assert result.returncode == 2, result.stdout + result.stderr
    assert "future review" in result.stdout.lower()


@pytest.mark.parametrize(
    "fault",
    [
        "missing_review_input",
        "wrong_review_input_hash",
        "wrong_review_input_artifact",
        "wrong_author_source",
        "stale_authored_artifact",
    ],
)
def test_authored_lineage_rejects_mismatched_or_stale_evidence(
    installed_cli, handoff, batch, fault
):
    value, write, save, root = handoff
    artifact = batch[3]
    group = value["groups"][0]
    if fault in ("missing_review_input", "wrong_review_input_hash", "wrong_review_input_artifact"):
        record = json.loads((root / "review-execution.json").read_bytes())
        if fault == "missing_review_input":
            record.pop("input_requirement_spec_ref")
        elif fault == "wrong_review_input_hash":
            record["input_requirement_spec_sha256"] = "0" * 64
        else:
            record["input_requirement_spec_ref"] = group["requirement_spec_ref"]
        group["review_ref"] = synthetic_execution(artifact, root, "review", record)
    elif fault == "wrong_author_source":
        authored = json.loads((root / "authored-requirements.json").read_bytes())
        authored["input_sha256"] = "0" * 64
        group["authored_requirement_spec_ref"] = artifact(
            "different-authored.json", authored, authored["schema_version"]
        )
    staging, attached = root / "staging", root / "attached"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    handoff_path = write()
    if fault == "stale_authored_artifact":
        assert (
            installed_cli(
                "batch",
                "attach-requirements",
                staging / "staging.json",
                handoff_path,
                "--directory",
                attached,
            ).returncode
            == 0
        )
        (root / "authored-requirements.json").write_bytes(b"{}")
        result = installed_cli(
            "batch", "finalize", attached / "attachment.json", "--directory", root / "final"
        )
        assert not (root / "final/manifest.json").exists()
    else:
        result = installed_cli(
            "batch",
            "attach-requirements",
            staging / "staging.json",
            handoff_path,
            "--directory",
            attached,
        )
        assert not attached.exists()
    assert result.returncode == 2, result.stdout + result.stderr


def test_execution_transcripts_can_use_their_own_retained_directory_layout(
    installed_cli, handoff, batch
):
    value, write, save, root = handoff
    artifact = batch[3]
    (root / "transcripts").mkdir()
    for operation in ("authoring", "review"):
        record = json.loads((root / (operation + "-execution.json")).read_bytes())
        transcript = json.loads((root / (operation + "-transcript.json")).read_bytes())
        record["transcript_ref"] = artifact(
            "transcripts/" + operation + ".json", transcript, transcript["schema_version"]
        )
        value["groups"][0][operation + "_ref"] = artifact(
            operation + "-execution.json", record, record["schema_version"]
        )
    staging, attached, final = root / "staging", root / "attached", root / "final"
    assert installed_cli("batch", "collect", save(), "--directory", staging).returncode == 0
    result = installed_cli(
        "batch", "attach-requirements", staging / "staging.json", write(), "--directory", attached
    )
    assert result.returncode == 0, result.stdout + result.stderr
    result = installed_cli("batch", "finalize", attached / "attachment.json", "--directory", final)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (final / "requirements/transcripts/review.json").read_bytes() == (
        root / "transcripts/review.json"
    ).read_bytes()
