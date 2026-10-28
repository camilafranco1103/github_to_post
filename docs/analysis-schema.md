# Analysis schema v1

`github_to_post.schemas.AnalysisDocument` is the canonical typed representation of one repository analysis. It is serialized as JSON; Markdown and optional YAML are derived from this model.

## Document sections

| Field | Purpose |
| --- | --- |
| `schema_version` | Integer schema version; this release emits `1`. |
| `repository` | GitHub owner, repository name, and URL. |
| `snapshot` | Selected ref and exact 40-character commit SHA analyzed. |
| `analyzed_at` | Timestamp of the analysis. |
| `technologies` | Language, framework, and tool findings marked as observed or inferred and linked to evidence IDs. |
| `evidence` | Repository-relative source path, concise observed fact, and extraction provenance. |
| `descriptions` | Evidence-linked descriptions with generation timestamps and optional LLM provider and model metadata. |
| `export` | Producer version, creation time, and output formats. |

Timestamps must include a timezone. Evidence paths use POSIX separators and cannot be absolute or traverse outside the repository. Every technology finding and description must declare whether its claim is observed or inferred and reference evidence present in the same document. Evidence IDs must be unique. Unknown fields and unsupported schema versions are rejected.

## Compatibility policy

Schema v1 is strict. Any change to field structure or meaning requires a new integer `schema_version`; readers reject unsupported versions instead of silently guessing or coercing. A future version that needs old documents must provide an explicit migration. Patch-level application releases do not change the schema version unless the schema itself changes.

The representative v1 JSON fixture lives at `tests/fixtures/analysis.v1.json`. Validate documents with `AnalysisDocument.model_validate_json(...)` and serialize with `model_dump_json(...)`.