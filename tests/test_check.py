from copy import deepcopy

import pytest

from fastapi import status
from fastapi.testclient import TestClient
from fastapi_pagination.utils import disable_installed_extensions_check

from app.main import app


disable_installed_extensions_check()
client = TestClient(app)

BASE_URL = "http://localhost:8000"
URL_CREATE_CHECK = BASE_URL + app.url_path_for("create_check")
URL_GET_CHECKS_LIST = BASE_URL + app.url_path_for("get_checks")


@pytest.mark.asyncio
async def test_create_check_success(
    check_data, get_headers_with_jwt, async_client
):
    response = await async_client.post(
        URL_CREATE_CHECK, json=check_data, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["total"] == 100
    assert response.json()["rest"] == 100
    assert response.json()["payment"]["amount"] == 200
    assert response.json()["payment"]["type"] == "cash"


@pytest.mark.asyncio
async def test_create_check_wrong_payment_type_fail(
    check_data, get_headers_with_jwt, async_client
):
    check_data = deepcopy(check_data)
    check_data["payment"]["type"] = "wrong_payment"
    response = await async_client.post(
        URL_CREATE_CHECK, json=check_data, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "Wrong payment type"


@pytest.mark.asyncio
async def test_create_check_not_enough_payment_fail(
    check_data, get_headers_with_jwt, async_client
):
    check_data = deepcopy(check_data)
    check_data["payment"]["amount"] = 0
    response = await async_client.post(
        URL_CREATE_CHECK, json=check_data, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "Not enough payment amount"


@pytest.mark.asyncio
async def test_create_check_not_authenticated_fail(check_data, async_client):
    response = await async_client.post(URL_CREATE_CHECK, json=check_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_checks_list_success_with_params_success(
    get_headers_with_jwt, check_query_params, async_client
):
    response = await async_client.get(
        URL_GET_CHECKS_LIST,
        headers=get_headers_with_jwt,
        params=check_query_params,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_checks_list_success(get_headers_with_jwt, async_client):
    response = await async_client.get(
        URL_GET_CHECKS_LIST, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_checks_list_not_authenticated_fail(async_client):
    response = await async_client.get(URL_GET_CHECKS_LIST)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_check_success(
    get_headers_with_jwt, async_client, check_data
):
    check_response = await async_client.post(
        URL_CREATE_CHECK, json=check_data, headers=get_headers_with_jwt
    )
    check = check_response.json()
    url_get_check = BASE_URL + app.url_path_for(
        "get_check", check_id=check["id"]
    )
    response = await async_client.get(
        url_get_check, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_check_not_authenticated_fail(
    get_headers_with_jwt, async_client, check_data
):
    check = await async_client.post(
        URL_CREATE_CHECK, json=check_data, headers=get_headers_with_jwt
    )
    url_get_check = BASE_URL + app.url_path_for(
        "get_check", check_id=check.json()["id"]
    )
    response = await async_client.get(url_get_check)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_check_not_enough_permission_fail(
    get_headers_with_jwt, async_client
):
    url_get_check = BASE_URL + app.url_path_for("get_check", check_id=1)
    response = await async_client.get(
        url_get_check, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not enough permission"


@pytest.mark.asyncio
async def test_get_check_does_not_exists_fail(
    get_headers_with_jwt, async_client
):
    url_get_check = BASE_URL + app.url_path_for("get_check", check_id=500)
    response = await async_client.get(
        url_get_check, headers=get_headers_with_jwt
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Check with id 500 does not exist"


@pytest.mark.asyncio
async def test_get_text_check_success(async_client):
    url_get_text_check = BASE_URL + app.url_path_for(
        "get_text_check", check_id=1
    )
    response = await async_client.get(url_get_text_check)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_text_check_not_exists_fail(async_client):
    url_get_text_check = BASE_URL + app.url_path_for(
        "get_text_check", check_id=500
    )
    response = await async_client.get(url_get_text_check)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Check with id 500 does not exist"
