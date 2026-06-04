class TestGetItem:
    def test_returns_item_when_found(self, client, mock_table):
        mock_table.get_item.return_value = {"Item": {"id": "123", "name": "widget"}}

        response = client.get("/items/123")

        assert response.status_code == 200
        assert response.json() == {"id": "123", "name": "widget"}
        mock_table.get_item.assert_called_once_with(Key={"id": "123"})

    def test_returns_404_when_not_found(self, client, mock_table):
        mock_table.get_item.return_value = {}

        response = client.get("/items/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

    def test_returns_404_when_item_is_none(self, client, mock_table):
        mock_table.get_item.return_value = {"Item": None}

        response = client.get("/items/abc")

        assert response.status_code == 404


class TestListItems:
    def test_returns_items(self, client, mock_table):
        items = [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}]
        mock_table.scan.return_value = {"Items": items, "Count": 2}

        response = client.get("/items")

        assert response.status_code == 200
        assert response.json() == {"items": items, "count": 2}
        mock_table.scan.assert_called_once_with(Limit=25)

    def test_returns_empty_list(self, client, mock_table):
        mock_table.scan.return_value = {"Items": [], "Count": 0}

        response = client.get("/items")

        assert response.status_code == 200
        assert response.json() == {"items": [], "count": 0}

    def test_custom_limit(self, client, mock_table):
        mock_table.scan.return_value = {"Items": [], "Count": 0}

        response = client.get("/items?limit=5")

        assert response.status_code == 200
        mock_table.scan.assert_called_once_with(Limit=5)

    def test_missing_keys_in_response(self, client, mock_table):
        mock_table.scan.return_value = {}

        response = client.get("/items")

        assert response.status_code == 200
        assert response.json() == {"items": [], "count": 0}


class TestHealth:
    def test_returns_ok(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "table" in data
