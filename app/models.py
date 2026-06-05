from pydantic import BaseModel


class ItemResponse(BaseModel):
    model_config = {"extra": "ignore"}

    id: str
    name: str


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    count: int
