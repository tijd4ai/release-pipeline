import pytest
from pydantic import ValidationError

from app.models import ItemListResponse, ItemResponse


class TestItemResponse:
    def test_valid_data(self):
        item = ItemResponse(id="1", name="widget")
        assert item.id == "1"
        assert item.name == "widget"

    def test_strips_extra_fields(self):
        item = ItemResponse.model_validate({"id": "1", "name": "widget", "secret": "s3cr3t"})
        assert item.id == "1"
        assert item.name == "widget"
        assert not hasattr(item, "secret")

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            ItemResponse(id="1")


class TestItemListResponse:
    def test_serialization(self):
        resp = ItemListResponse(
            items=[{"id": "1", "name": "a"}, {"id": "2", "name": "b"}],
            count=2,
        )
        data = resp.model_dump()
        assert data == {
            "items": [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}],
            "count": 2,
        }
