# Repository Guidelines

## Project Structure & Module Organization

The repository currently contains project guidance and installed agent skills, but no application code. As the project grows, keep application code in a clearly named source directory (such as `src/`), automated checks in `tests/` or alongside the modules they cover, and static files in `assets/`. Group related features together and avoid placing generated output or local secrets in source control.

## Product Scope & Data Flow

- Build the repository analyzer as a Python ETL project. Its initial input is a Python list of `owner/repo` identifiers containing one repository. Use `coin-or/pulp` as the initial public example repository unless the user changes it.
- Run the MVP locally. Use Airflow as the local workflow orchestrator while keeping extraction, normalization, validation, and export logic callable independently of Airflow. Defer AWS hosting and deployment decisions.
- Select the source snapshot in this order: latest project version/release tag when available; otherwise the `prod` branch, then `main`, then the repository default branch. Record the selected ref and exact commit SHA with every result.
- Public repositories do not require authentication. Before accessing a private repository, check for an already authenticated GitHub CLI (`gh`) user; if none is configured, report the issue and stop.
- Use Pydantic AI as the provider-agnostic LLM integration layer. Configure OpenAI as the initial provider through its Responses API integration; keep provider and model names in application configuration, and keep API keys in environment variables rather than tracked files. Use typed Pydantic output models for structured semantic results and retain deterministic validation before export.
- Use an LLM for semantic repository descriptions. Allow public repository content to be sent to the configured external LLM by default. Block private repository content from external LLM services by default. Make the policy configurable so the user can also disable external content transfer for public repositories. If external transfer is blocked and no local LLM is configured, produce deterministic findings and clearly mark semantic analysis as limited; never silently send blocked content.
- Generate a versioned JSON document and a Markdown report for each successful run. Treat the normalized JSON model as canonical; derive Markdown and any optional YAML export from that same model.
- Database output is optional and deferred. Keep the file exports usable without a database. When database support is designed, store its schema as versioned SQL DDL/migrations in the repository (for example, under `db/migrations/`).
- Preserve evidence for extracted facts where practical, including source file references, and distinguish observed facts from inferred conclusions.
- Keep credentials, tokens, and machine-specific configuration out of source control and generated documentation.

## Work Tracking

Use GitHub Projects as the planning and progress board, owned by the personal GitHub account already configured in `gh` when the remote repository is initialized. Represent actionable work as GitHub Issues, break larger issues into sub-issues, and link implementation Pull Requests to their Issues. Use these initial Project status values: `Backlog`, `Ready`, `In Progress`, `In Review`, `Testing`, `Done`, and `Blocked`. Use Project automation to keep issue and pull request status current where appropriate.

## Branch & Deployment Workflow

- Keep `dev` as the long-lived integration branch and keep it current with merged work.
- Create one short-lived branch for each Issue or feature from `dev`, using a name such as `feature/<issue-number>-<slug>` or `fix/<issue-number>-<slug>`. Open a Pull Request back to `dev`, link it to the Issue, require CI checks to pass, and delete the temporary branch after merge.
- Use GitHub Environments named `development`, `test`, and `production` for deployment stages; do not create long-lived `test` or `prod` branches for environment promotion.
- Deploy the integrated `dev` state to development. Promote the same immutable build/artifact to test, and promote that tested artifact to production only after test validation and an explicit production promotion step. Tag the production release on the deployed commit.
- Keep Project work statuses separate from deployment environments. Configure branch protection and Actions when the remote repository is initialized.

## Build, Test, and Development Commands

The project uses uv with a committed uv.lock. Run `uv sync --locked` to install dependencies and `uv run --locked pytest` to run tests from the repository root. GitHub Actions runs the test suite for Python 3.12, 3.13, and 3.14 on pull requests to `dev` and pushes to `dev`.

## Coding Style & Naming Conventions

No language-specific formatter or lint configuration exists yet. Follow the conventions of the chosen language, use consistent indentation, and run the formatter and linter configured by the project before submitting changes. Prefer descriptive, lowercase filenames; use the language's common naming style for modules, types, and functions. Keep functions focused and configuration explicit.

## Testing Guidelines

Place Python tests under `tests/` using `test_<feature>.py` names. Add tests for new behavior and regressions, and keep the documented `uv run --locked pytest` command working.

## Commit & Pull Request Guidelines

Git history is not available in this working directory, so no repository-specific commit convention can be inferred. Use short imperative commit subjects, such as `Add input validation`, and consider Conventional Commit prefixes when useful (for example, `fix: handle empty input`). Pull requests should explain the change and its motivation, list validation performed, link related issues, and include screenshots for user-visible changes.

## Security & Configuration

Do not commit credentials, tokens, generated private repository contents, or machine-specific configuration. Provide safe example configuration where needed, and document required environment variables without including their secret values.