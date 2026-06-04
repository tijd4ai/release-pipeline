from fastapi import FastAPI, HTTPException
from boto3.dynamodb.conditions import Key

from app.database import table
from app.config import settings

app = FastAPI(title="DynamoDB API")


@app.get("/items/{item_id}")
def get_item(item_id: str):
    response = table.get_item(Key={"id": item_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items")
def list_items(limit: int = 25):
    response = table.scan(Limit=limit)
    return {"items": response.get("Items", []), "count": response.get("Count", 0)}


@app.get("/health")
def health():
    return {"status": "ok", "table": settings.dynamodb_table}
