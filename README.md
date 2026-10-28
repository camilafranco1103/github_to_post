# GitHub to Post

A local Python ETL that analyzes GitHub repositories and produces detailed, evidence-backed project documentation.

## Planned outputs

- Versioned JSON as the canonical analysis format.
- Markdown project reports.
- Optional YAML exports.
- Database storage and its DDL are deferred.

## Initial design

- A Python list of owner/repo values is the initial source.
- The first public fixture is coin-or/pulp.
- Source selection prefers the latest release tag, then prod, main, and the default branch. The selected ref and commit SHA are recorded.
- Airflow runs the local pipeline; ETL stages remain independently callable Python code.
- Pydantic AI provides the LLM interface, initially configured for OpenAI Responses.
- Private repository content is not sent to external models by default. This policy is configurable for all repositories.
- The Python package scaffold is ready; repository analysis stages are being implemented through the active GitHub issues.

## Local setup

Requirements: Python 3.12, 3.13, or 3.14, and uv.

From the repository root, sync the locked environment:

    uv sync --locked

The initial command lists the configured repositories. The ETL stages will be added in the follow-up issues:

    uv run github-to-post

Add source repositories in src/github_to_post/sources.py. Keep local credentials in .env; the tracked .env.example contains no secret.

uv.lock pins the resolved project dependencies. After changing pyproject.toml, refresh it with uv lock and verify it with uv lock --check.

## Work tracking

GitHub Issues and the personal GitHub Project track work. Use a short-lived branch per issue, branch from dev, and open a pull request back to dev. Validate changes in the test environment before promotion to prod.

The project-local agent skills are pinned in skills-lock.json and stored under .agents/skills/.


## Testing

Run the test suite locally with the locked development environment:

    uv sync --locked
    uv run --locked pytest

GitHub Actions runs the same test command for Python 3.12, 3.13, and 3.14 on pull requests targeting `dev` and pushes to `dev`.
## Canonical analysis schema

The versioned Pydantic models in `github_to_post.schemas` define the canonical analysis document. See [the schema v1 contract](docs/analysis-schema.md) for fields, evidence traceability, and compatibility rules. Validate serialized documents with `AnalysisDocument.model_validate_json(...)`.