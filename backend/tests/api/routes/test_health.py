from fastapi.testclient import TestClient

from app.core.config import settings


class TestIntegration:
    def test_it_returns_200_when_calling_healthz(
        self,
        client: TestClient,
    ) -> None:
        response = client.get(f"{settings.API_V1_STR}/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "pass"}

    def test_it_returns_200_when_calling_readyz(
        self,
        client: TestClient,
    ) -> None:
        response = client.get(f"{settings.API_V1_STR}/readyz")
        assert response.status_code == 200
        assert response.json() == {
            "status": "pass",
            "checks": {"postgres:connections": [{"status": "pass"}]},
        }
