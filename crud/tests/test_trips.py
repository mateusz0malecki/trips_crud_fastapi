import json


def test_new_trip(client):
    data = {
        "trip_id": 1,
        "name": "trip",
        "email": "test@email.com",
        "description": "trip to nowhere",
        "completeness": False,
        "contact": True
    }
    response = client.post('/trips/', json.dumps(data))
    assert response.status_code == 201
    assert response.json()["email"] == "test@email.com"
    assert response.json()["contact"] is True


def test_get_trip(client):
    response = client.get("/trips/1")
    assert response.status_code == 200
    assert response.json()["description"] == "trip to nowhere"
    assert response.json()["completeness"] is not True


def test_edit_trip(client):
    data = {
        "name": "trip2",
        "email": "test@email.com",
        "description": "trip to nowhere",
        "completeness": True,
        "contact": True
    }
    response = client.put("/trips/1", json.dumps(data))
    assert response.status_code == 202
    assert response.json()["name"] == "trip2"
    assert response.json()["completeness"] is True
    assert response.json()["email"] == "test@email.com"


def test_delete_trip(client):
    response = client.delete("/trips/1")
    assert response.status_code == 204


def test_all_trips(client):
    response = client.get("/trips/")
    assert response.status_code == 200
    assert len(response.json()) == 0
