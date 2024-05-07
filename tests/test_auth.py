from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

BASE_URL = "http://localhost:8000"
URL_GET_ACCESS_TOKEN = BASE_URL + app.url_path_for("get_access_token")


async def test_get_access_token_success(async_client, create_test_user):
    response = await async_client.post(
        URL_GET_ACCESS_TOKEN, data=create_test_user
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_get_access_token_invalid_credentials_fail(async_client):
    response = await async_client.post(
        URL_GET_ACCESS_TOKEN,
        data={"username": "invalid_name", "password": "invalid_pass"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Invalid username or password"
