import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.hash import Hash


def test_new_user(client):
    data = {
        "name": "user",
        "email": "user@hihi@com",
        "password": "password",
        "is_active": True,
        "is_admin": False
    }
    response = client.post("/users/", json.dumps(data))
    assert response.json()["email"] == "user@hihi@com"
    assert response.json()["is_admin"] is False
    assert response.status_code == 201


def test_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["is_admin"] is True
    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json()["is_admin"] is not True


def test_edit_user(client):
    data = {
        "email": "new_user@hihi@com",
        "password": "password",
    }
    response = client.put("/users/2", json.dumps(data))
    assert response.status_code == 202
    assert response.json()["email"] == "new_user@hihi@com"
    password_assertion = Hash.verify_password("password", response.json()["password"])
    assert password_assertion is True


def test_edit_user_status(client):
    response = client.put("/users/active/2")
    assert response.status_code == 202
    assert response.json()["is_active"] is False
    response = client.put("/users/aaaa/2")
    assert response.status_code == 400
    response = client.put("/users/active/1")
    assert response.status_code == 400


def test_delete_user(client):
    response = client.delete("/users/2")
    assert response.status_code == 204
