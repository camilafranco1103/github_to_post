"""Versioned, evidence-backed analysis document models."""

from datetime import datetime
from pathlib import PurePosixPath
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)


def require_timezone(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    return value


Timestamp = Annotated[datetime, AfterValidator(require_timezone)]


class SchemaModel(BaseModel):
    """Base for immutable models that reject undeclared fields."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class RepositoryIdentity(SchemaModel):
    owner: str = Field(min_length=1)
    name: str = Field(min_length=1)
    url: HttpUrl

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


class RepositorySnapshot(SchemaModel):
    ref: str = Field(min_length=1)
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")


class ExtractionProvenance(SchemaModel):
    extractor: str = Field(min_length=1)
    extractor_version: str = Field(min_length=1)
    method: str = Field(min_length=1)
    extracted_at: Timestamp


class Evidence(SchemaModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9._-]*$")
    source_path: str = Field(min_length=1)
    fact: str = Field(min_length=1)
    provenance: ExtractionProvenance

    @field_validator("source_path")
    @classmethod
    def validate_repository_relative_path(cls, value: str) -> str:
        first_segment = value.split("/", 1)[0]
        if "\\" in value or value.startswith("/") or ":" in first_segment:
            raise ValueError("source_path must be a repository-relative POSIX path")
        if any(part in {"", ".", ".."} for part in value.split("/")):
            raise ValueError("source_path must not contain empty, current, or parent path segments")
        if PurePosixPath(value).is_absolute():
            raise ValueError("source_path must be a repository-relative POSIX path")
        return value


class EvidenceLinkedClaim(SchemaModel):
    claim_type: Literal["observed", "inferred"]
    evidence_ids: list[str] = Field(min_length=1)


class TechnologyFinding(EvidenceLinkedClaim):
    category: Literal["language", "framework", "tool"]
    name: str = Field(min_length=1)
    version: str | None = None


class RepositoryDescription(EvidenceLinkedClaim):
    text: str = Field(min_length=1)
    generated_at: Timestamp
    provider: str | None = None
    model: str | None = None

    @model_validator(mode="after")
    def require_provider_and_model_together(self) -> "RepositoryDescription":
        if (self.provider is None) != (self.model is None):
            raise ValueError("provider and model must be provided together")
        return self


class ExportMetadata(SchemaModel):
    producer_version: str = Field(min_length=1)
    created_at: Timestamp
    formats: list[Literal["json", "markdown", "yaml"]] = Field(min_length=1)


class AnalysisDocument(SchemaModel):
    """Canonical schema v1 document for one immutable repository snapshot."""

    schema_version: Literal[1] = 1
    repository: RepositoryIdentity
    snapshot: RepositorySnapshot
    analyzed_at: Timestamp
    technologies: list[TechnologyFinding] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    descriptions: list[RepositoryDescription] = Field(default_factory=list)
    export: ExportMetadata

    @model_validator(mode="after")
    def validate_evidence_references(self) -> "AnalysisDocument":
        evidence_ids = [item.id for item in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence IDs must be unique")

        known_ids = set(evidence_ids)
        referenced_ids = {
            evidence_id
            for item in [*self.technologies, *self.descriptions]
            for evidence_id in item.evidence_ids
        }
        unknown_ids = sorted(referenced_ids - known_ids)
        if unknown_ids:
            raise ValueError(f"unknown evidence IDs: {', '.join(unknown_ids)}")
        return self