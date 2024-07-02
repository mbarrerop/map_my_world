import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_data():
    # Crear una categoría de prueba
    category = {"name": "Park", "description": "A public park"}
    response = client.post("/api/v1/categories", json=category)
    category_id = response.json()["id"]

    # Crear una ubicación de prueba
    location = {
        "name": "Central Park",
        "description": "A large public park in New York City",
        "latitude": 40.785091,
        "longitude": -73.968285,
        "category_id": category_id
    }
    response = client.post("/api/v1/locations", json=location)
    location_id = response.json()["id"]

    review = {
        "location_id": location_id,
        "category_id": category_id,
        "review_notes": "Initial review"
    }
    response = client.post("/api/v1/reviews", json=review)
    review_id = response.json()["id"]

    yield {"category_id": category_id, "location_id": location_id, "review_id": review_id}

def test_get_review_by_id(test_data):
    review_id = test_data["review_id"]
    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()["id"] == review_id

def test_create_review(test_data):
    new_review = {
        "location_id": test_data["location_id"],
        "category_id": test_data["category_id"],
        "review_notes": "Test review"
    }
    response = client.post("/api/v1/reviews", json=new_review)
    assert response.status_code == 200
    assert response.json()["review_notes"] == "Test review"

def test_update_review(test_data):
    review_id = test_data["review_id"]
    update_review = {
        "review_notes": "Updated review"
    }
    response = client.put(f"/api/v1/reviews/{review_id}", json=update_review)
    assert response.status_code == 200
    assert response.json()["review_notes"] == "Updated review"

def test_get_recommendations():
    response = client.get("/api/v1/reviews/recommendations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
