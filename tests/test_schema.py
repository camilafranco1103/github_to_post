import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from github_to_post.schemas import AnalysisDocument


FIXTURE = Path(__file__).parent / "fixtures" / "analysis.v1.json"


def test_analysis_fixture_validates_and_round_trips() -> None:
    document = AnalysisDocument.model_validate_json(FIXTURE.read_text(encoding="utf-8"))

    assert document.schema_version == 1
    assert document.repository.full_name == "coin-or/pulp"
    assert document.snapshot.commit_sha == "0123456789abcdef0123456789abcdef01234567"
    assert document.technologies[0].evidence_ids == ["evidence-python"]
    assert AnalysisDocument.model_validate_json(document.model_dump_json()) == document


@pytest.mark.parametrize(
    "path",
    [
        "/absolute/file.py",
        "../outside.py",
        "src/../../outside.py",
        r"C:\repo\file.py",
    ],
)
def test_evidence_rejects_non_repository_paths(path: str) -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["evidence"][0]["source_path"] = path

    with pytest.raises(ValidationError):
        AnalysisDocument.model_validate(payload)


def test_analysis_rejects_duplicate_evidence_ids() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["evidence"].append(payload["evidence"][0])

    with pytest.raises(ValidationError, match="unique"):
        AnalysisDocument.model_validate(payload)


def test_analysis_rejects_unresolved_evidence_references() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["technologies"][0]["evidence_ids"] = ["missing-evidence"]

    with pytest.raises(ValidationError, match="unknown evidence"):
        AnalysisDocument.model_validate(payload)


def test_analysis_rejects_unsupported_schema_version() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["schema_version"] = 2

    with pytest.raises(ValidationError):
        AnalysisDocument.model_validate(payload)


def test_analysis_rejects_naive_timestamps() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["analyzed_at"] = "2026-10-28T12:00:00"

    with pytest.raises(ValidationError, match="timezone"):
        AnalysisDocument.model_validate(payload)


def test_analysis_rejects_unknown_fields() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["unexpected"] = True

    with pytest.raises(ValidationError, match="extra_forbidden"):
        AnalysisDocument.model_validate(payload)


def test_description_requires_provider_and_model_together() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["descriptions"][0]["provider"] = "openai"

    with pytest.raises(ValidationError, match="provided together"):
        AnalysisDocument.model_validate(payload)