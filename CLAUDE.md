# Release Pipeline - FastAPI + DynamoDB

## Stack
- Python, FastAPI, boto3
- AWS DynamoDB
- GitHub Actions for CI/CD
- **uv** for Python package management — always use `uv` instead of `pip` (e.g. `uv add`, `uv run`, `uv sync`)

## Workflow
For any feature request:
1. Use the **planner** agent to create an implementation plan, then pause for my approval
2. Use the **architect** agent to validate the design
3. Use the **developer** agent to implement it
4. Use the **reviewer** agent to review all changes before finishing
