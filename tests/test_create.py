import pytest

from tests.settings import client


@pytest.mark.asyncio
async def test_create_user():
    response = client.post(
        "/users/create/",
        json={"first_name": "Jamoliddin", "last_name": "Bakhriddinov"},
    )

    assert response.status_code == 201
