import random
import asyncio

import pytest

from httpx import AsyncClient

from app.main import app


BASE_URL = "http://localhost:8000"
URL_USER_LOGIN = BASE_URL + app.url_path_for("get_access_token")
URL_CREATE_USER = BASE_URL + app.url_path_for("create_user")


client = AsyncClient(app=app, base_url=BASE_URL)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


TEST_USER_DATA = {
    "first_name": "test",
    "last_name": "test",
    "username": "name" + str(random.randint(1, 99999999)),
    "password": "Password11",
}

TEST_CHECK_CREATE_DATA = {
    "products": [
        {"name": "test_product1", "price": 20, "quantity": 3},
        {"name": "test_product2", "price": 20, "quantity": 2},
    ],
    "payment": {"type": "cash", "amount": 200},
}


@pytest.fixture()
def user_data():
    return TEST_USER_DATA


@pytest.fixture()
def check_data():
    return TEST_CHECK_CREATE_DATA


@pytest.fixture()
async def create_test_user(async_client):
    user_data = {
        "first_name": "test",
        "last_name": "test",
        "username": "Test username" + str(random.randint(1, 99999999)),
        "password": "Password11",
    }
    await async_client.post(URL_CREATE_USER, json=user_data)
    return user_data


@pytest.fixture()
async def get_headers_with_jwt(async_client, create_test_user):
    user_data = create_test_user
    data = {
        "username": user_data["username"],
        "password": user_data["password"],
    }
    response = await async_client.post(URL_USER_LOGIN, data=data)
    jwt = response.json()
    headers = {
        "Authorization": f"Bearer {jwt['access_token']}",
    }
    return headers


@pytest.fixture()
def sign_up_data():
    user_data = create_test_user()
    return {
        "username": user_data["username"],
        "password": user_data["password"],
    }


@pytest.fixture()
def check_query_params():
    return {
        "total__gte": 20.00,
        "total__lte": 200.00,
        "created_at__gte": "2024-05-06",
        "created_at__lte": "2024-05-07",
        "payment_type": "cash",
        "page": 1,
        "size": 1,
    }
