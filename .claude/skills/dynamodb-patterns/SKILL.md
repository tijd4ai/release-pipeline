---
name: dynamodb-patterns
description: DynamoDB access patterns, query vs scan rules, Decimal handling, moto test setup, and single-table conventions for this project.
---

# DynamoDB Patterns

## Access rules
- All DynamoDB access goes through `app/database.py` — never import boto3 directly in routes or services.
- Use `table.get_item(Key={...})` for single-item lookups by partition key.
- Use `table.query()` with `KeyConditionExpression` when you know the partition key and want multiple items — never `scan()` for known-key access.
- Reserve `table.scan()` for admin/list-all operations only. Always pass `Limit` and handle `LastEvaluatedKey` for pagination.
- Never use `FilterExpression` as a substitute for a query — it scans first, then filters, so it doesn't save read capacity.

## Pydantic response models
- Define models in `app/models.py` with `model_config = {"extra": "ignore"}` to strip unexpected DynamoDB attributes from API responses.
- Use `ModelClass.model_validate(item)` explicitly in route bodies rather than relying solely on `response_model=` for the conversion.
- Use return type annotations (`-> ItemResponse`) — FastAPI infers the response model.

## Decimal handling
- DynamoDB returns `Decimal` for all numeric values, not `int` or `float`.
- For numeric model fields, add a Pydantic `BeforeValidator` to coerce:
  ```python
  from decimal import Decimal
  from typing import Annotated
  from pydantic import BeforeValidator

  CoercedInt = Annotated[int, BeforeValidator(lambda v: int(v) if isinstance(v, Decimal) else v)]
  CoercedFloat = Annotated[float, BeforeValidator(lambda v: float(v) if isinstance(v, Decimal) else v)]
  ```
- When writing numeric values to DynamoDB, convert `float` to `Decimal` first — boto3 rejects raw floats.

## Testing with moto
- Use `moto` to mock DynamoDB in integration tests. Basic setup:
  ```python
  import boto3
  import pytest
  from moto import mock_aws

  @pytest.fixture()
  def dynamodb_table():
      with mock_aws():
          client = boto3.resource("dynamodb", region_name="us-east-1")
          table = client.create_table(
              TableName="items",
              KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
              AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
              BillingMode="PAY_PER_REQUEST",
          )
          yield table
  ```
- For unit tests, the project uses `unittest.mock.patch("app.main.table")` — see `tests/conftest.py`.
- Prefer mock-patching for fast unit tests; use moto for integration tests that validate actual DynamoDB behavior (conditional writes, queries, pagination).

## Key schema conventions
- Partition key is always `id` (string).
- If a GSI is needed, name it `{attribute}-index` (e.g., `name-index`).
- Use `PAY_PER_REQUEST` billing for dev/test; provisioned for production (set via environment config).
