from httpx import AsyncClient

from app import __version__


async def test_liveliness_check(client: AsyncClient) -> None:
    response = await client.get("/livez")
    assert response.status_code == 200


async def test_readiness_check(client: AsyncClient) -> None:
    response = await client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["message"] == "ok"
    assert response.json()["version"] == __version__
    assert response.json()["t"]
