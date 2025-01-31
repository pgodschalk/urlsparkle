from fastapi.testclient import TestClient

from app.core.config import settings


class TestIntegration:
    def test_it_returns_204_when_calling_healthz(
        self,
        client: TestClient,
    ) -> None:
        response = client.head(f"{settings.API_V1_STR}/healthz")
        assert response.status_code == 204
        assert response.text == ""

    def test_it_returns_204_when_calling_readyz(
        self,
        client: TestClient,
    ) -> None:
        response = client.head(f"{settings.API_V1_STR}/readyz")
        assert response.status_code == 204
        assert response.text == ""
