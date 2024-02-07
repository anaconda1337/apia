import pytest

from app.constants import API_V1_PREFIX
from app.constants import API_V1_HEALTH_CHECK


URL = f"{API_V1_PREFIX}{API_V1_HEALTH_CHECK}"


@pytest.mark.asyncio
async def test_health_check_unauthenticated_token_not_provided(client):
    response = client.get(URL)

    assert response.status_code == 401
    assert response.json() == {"detail": "Bearer authentication required"}


@pytest.mark.asyncio
async def test_health_check_unauthenticated_token_invalid(
        client,
        firebase_invalid_id_token
):
    response = client.get(
        url=URL,
        headers=firebase_invalid_id_token
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials. The provided ID Token is not valid."}  # noqa: E501


@pytest.mark.asyncio
async def test_health_check_success(
        client,
        authentication_headers,
        httpx_mock
):
    response = client.get(
        url=URL,
        headers=authentication_headers
    )

    httpx_mock.add_response(
        url="https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo",  # noqa: E501
        json={
            "users": [
                {
                    "localId": "123",
                    "email": "test@test.gmail.com",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "name": "fastapi-boilerplate",
        "version": "0.1.0",
        "timestamp": "2021-01-01T00:00:00+00:00"
    }
