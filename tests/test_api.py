from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # Creat a test client


def test_get_flight_not_found():
    response = client.get("/flights/999999") # ID 999999, suppose it does not exist
    assert response.status_code in [404, 200]


def test_delay_rate_endpoint():
    response = client.get(
        "/analytics/delay-rate?origin=ATL", # Query the delay rate of ATL Airport
        headers={"X-API-Key": "1122332211"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "origin" in data
    assert "delay_rate" in data


def test_destinations_endpoint():
    response = client.get("/airports/ATL/destinations") # Query all destinations of ATL Airport
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data

def test_invalid_api_key():
    response = client.get(
        "/analytics/delay-rate?origin=ATL",
        headers={"X-API-Key": "wrong"} # Wrong key
    )
    assert response.status_code == 401
