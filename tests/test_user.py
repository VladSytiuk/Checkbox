from copy import deepcopy

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

BASE_URL = "http://localhost:8000"
URL_CREATE_USER = BASE_URL + app.url_path_for("create_user")


def test_create_user_success(user_data):
    response = client.post(URL_CREATE_USER, json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert (
        response.json()
        == f"User with username {user_data['username']} has been created successfully"
    )


def test_create_user_with_username_which_exists_fail(user_data):
    response = client.post(URL_CREATE_USER, json=user_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response.json()["detail"]
        == f"User with username {user_data['username']} already exist"
    )
