import pytest

def test_create_hero(client):
    r = client.post("/api/v1/heroes", json={"name": "Deadpond", "secret_name": "Dive Wilson"})
    assert r.status_code == 201
    assert r.json()["name"] == "Deadpond"
    assert r.json()["status"] == "active"

def test_read_hero_not_found(client):
    r = client.get("/api/v1/heroes/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "Hero not found"}

@pytest.mark.parametrize("payload", [
    {}, {"name": "X"},
    {"name": "X", "secret_name": "y", "age": "old"},
    {"name": "X", "secret_name": "y", "age": -5},
    {"name": "X", "secret_name": "y", "status": "dead"},
])
def test_create_hero_invalid(client, payload):
    assert client.post("/api/v1/heroes", json=payload).status_code == 422
