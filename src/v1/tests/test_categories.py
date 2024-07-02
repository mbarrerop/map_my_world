from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_category_by_id():
    new_category = {"name": "Museum", "description": "A category for museums"}
    response = client.post("/api/v1/categories", json=new_category)
    category_id = response.json()["id"]

    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["id"] == category_id

# Test for creating a new category
def test_create_category():
    new_category = {"name": "Zoo", "description": "A category for zoos"}
    response = client.post("/api/v1/categories", json=new_category)
    assert response.status_code == 201
    assert response.json()["name"] == "Zoo"