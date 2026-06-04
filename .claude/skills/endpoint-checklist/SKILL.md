---
name: endpoint-checklist
description: Step-by-step checklist for adding a new FastAPI route — schema, route, tests, and codebase map update.
---

# Endpoint Checklist

Follow these steps when adding a new endpoint.

## 1. Response/request models — `app/models.py`
- Define Pydantic `BaseModel` classes for request body (if POST/PUT/PATCH) and response.
- Set `model_config = {"extra": "ignore"}` on response models to strip unexpected DynamoDB fields.
- Use `str` for DynamoDB string attributes; use `CoercedInt`/`CoercedFloat` for numeric attributes (see dynamodb-patterns skill).

## 2. Route — `app/main.py`
- Import models from `app.models`.
- Use return type annotation (`-> MyResponse`) — FastAPI infers the response model.
- Call `Model.model_validate(item)` explicitly in the route body.
- Use `table` from `app.database` for DynamoDB access — never import boto3 directly.
- Raise `HTTPException` for error cases (404, 400, etc.) at the route level.
- For query parameters with bounds, use `Query(default=..., ge=..., le=...)`.

## 3. Tests — `tests/test_main.py`
- Add a test class named `Test<EndpointName>`.
- Cover: happy path, not-found/error cases, extra-field stripping, edge cases.
- Use the `client` and `mock_table` fixtures from `conftest.py`.
- Mock the specific DynamoDB method (`get_item`, `query`, `scan`, `put_item`, etc.) on `mock_table`.

## 4. Model tests — `tests/test_models.py`
- Test valid construction.
- Test that extra fields are stripped.
- Test that missing required fields raise `ValidationError`.

## 5. Update codebase map
- If the endpoint introduces new files, update the `## Codebase Map` section in `CLAUDE.md`.

## 6. Verify
- Run `uv run pytest -v` and confirm all tests pass.
