from fastapi import status
from fastapi.testclient import TestClient


from app.main import app


client = TestClient(app)

BASE_URL = "http://localhost:8000"
URL_GET_ACCESS_TOKEN = BASE_URL + app.url_path_for("get_access_token")


def test_get_access_token_success(sign_up_data):
    response = client.post(URL_GET_ACCESS_TOKEN, data=sign_up_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_get_access_token_invalid_credentials_fail():
    response = client.post(
        URL_GET_ACCESS_TOKEN,
        data={"username": "invalid_name", "password": "invalid_pass"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Invalid username or password"
