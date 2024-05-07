import pytest

from fastapi import status

from app.main import app


BASE_URL = "http://localhost:8000"
URL_CREATE_USER = BASE_URL + app.url_path_for("create_user")


@pytest.mark.asyncio
async def test_create_user_success(async_client, user_data):
    response = await async_client.post(URL_CREATE_USER, json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert (
        response.json()
        == f"User with username {user_data['username']} has been created successfully"
    )


@pytest.mark.asyncio
async def test_create_user_with_username_which_exists_fail(
    async_client, user_data
):
    response = await async_client.post(url=URL_CREATE_USER, json=user_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response.json()["detail"]
        == f"User with username {user_data['username']} already exist"
    )
