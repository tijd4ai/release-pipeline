# Release Pipeline - FastAPI + DynamoDB

## Stack
- Python, FastAPI, boto3
- AWS DynamoDB
- GitHub Actions for CI/CD
- **uv** for Python package management — always use `uv` instead of `pip` (e.g. `uv add`, `uv run`, `uv sync`)

## Workflow
For any non-trivial feature request (new endpoints, schema changes, new integrations):
1. Use the **planner** agent to create an implementation plan, then pause for my approval
2. Use the **architect** agent to validate the design
3. Use the **developer** agent to implement it
4. If the change involves CI/CD, infra, or deployment, use the **devops** agent for those parts
5. Use the **reviewer** agent to review all changes before finishing
6. If the reviewer finds issues, send them back to the **developer** (or **devops**) to fix, then re-run the **reviewer**

For small changes (typos, config tweaks, single-line fixes): skip directly to the **developer** agent, then run the **reviewer**.
For infra/pipeline-only changes: skip directly to the **devops** agent, then run the **reviewer**.

## Codebase Map

```
app/
  main.py          — FastAPI app, route definitions (GET /items/{id}, GET /items, GET /health)
  models.py        — Pydantic request/response schemas
  database.py      — DynamoDB client setup via boto3, exports `table`
  config.py        — env-based settings using pydantic-settings (prefix APP_)

tests/
  conftest.py      — pytest fixtures (mock_table, client)
  test_main.py     — endpoint tests using mocked DynamoDB table
  test_models.py   — model unit tests

.claude/agents/    — Claude Code subagent definitions (planner, architect, developer, reviewer, devops)
.claude/skills/    — On-demand skill definitions (dynamodb-patterns, endpoint-checklist, github-actions-deploy)

.github/workflows/ — GitHub Actions CI/CD pipelines
pyproject.toml     — project metadata, dependencies, ruff config
```

### Conventions
- All DynamoDB access goes through `app/database.py` — never raw boto3 in routes
- Errors: raise `HTTPException` at route level
- Tests mock the DynamoDB table via `unittest.mock.patch`
- Use `uv` for package management, never `pip`
