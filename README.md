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
- The project is in its planning and bootstrap stage; the ETL implementation has not started.

## Work tracking

GitHub Issues and the personal GitHub Project track work. Use a short-lived branch per issue, branch from dev, and open a pull request back to dev. Validate changes in the test environment before promotion to prod.

The project-local agent skills are pinned in skills-lock.json and stored under .agents/skills/.
