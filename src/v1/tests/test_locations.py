import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture
def create_test_location():
    category = {"name": "Park", "description": "A public park"}
    response = client.post("/api/v1/categories", json=category)
    category_id = response.json()["id"]

    location = {
        "name": "Central Park",
        "description": "A large public park in New York City",
        "latitude": 40.785091,
        "longitude": -73.968285,
        "category_id": category_id
    }
    response = client.post("/api/v1/locations", json=location)
    return response.json()

def test_get_location_by_id(create_test_location):
    location_id = create_test_location["id"]
    response = client.get(f"/api/v1/locations/{location_id}")
    assert response.status_code == 200
    assert response.json()["id"] == location_id

def test_create_location():
    category = {"name": "Park", "description": "A public park"}
    response = client.post("/api/v1/categories", json=category)
    category_id = response.json()["id"]

    new_location = {
        "name": "Brooklyn Bridge Park",
        "description": "A waterfront park in Brooklyn",
        "latitude": 40.700292,
        "longitude": -73.996807,
        "category_id": category_id
    }
    response = client.post("/api/v1/locations", json=new_location)
    assert response.status_code == 200
    assert response.json()["name"] == "Brooklyn Bridge Park"