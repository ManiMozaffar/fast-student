import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from fast_acl.acl.role import UserRoles
from fast_acl.app import app, get_permission_setting
from fast_acl.db import Database
from fast_acl.schema import TokenData
from fast_acl.settings import setting
from fast_acl.utils import pydantic_to_dict
from tests.mock import mock_permission_setting


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="class")
async def http_client():
    app.dependency_overrides[get_permission_setting] = mock_permission_setting
    async with AsyncClient(
        app=app, base_url=f"http://test/v{setting.VERSION}"
    ) as client:
        await app.router.startup()
        yield client
        await app.router.shutdown()


@pytest_asyncio.fixture(scope="class")
async def student_client(http_client: AsyncClient):
    student = Database.read_students()[0]
    data = TokenData(user_id=student.user_id, role=UserRoles.STUDENT)
    response = await http_client.post(
        "/token",
        json=pydantic_to_dict(data),
    )
    assert response.status_code == 200
    http_client.headers.update(
        {"Authorization": f"Bearer {response.json()['access_token']}"}
    )
    yield http_client
