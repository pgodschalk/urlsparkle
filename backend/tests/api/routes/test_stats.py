from fastapi.testclient import TestClient

from app.core.config import settings


class TestIntegration:
    def test_it_returns_stats_when_using_existing_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com"}
        shorten_response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        stats_response = client.get(
            f"{settings.API_V1_STR}/{shorten_response.json().get('shortcode')}/stats"
        )
        assert stats_response.status_code == 200
        content = stats_response.json()
        assert "created" in content
        assert "created" != None
        assert "lastRedirect" in content
        assert "redirectCount" in content

    def test_it_returns_incremented_stats_when_using_existing_and_used_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com"}
        shorten_response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        client.get(
            f"{settings.API_V1_STR}/{shorten_response.json().get('shortcode')}",
            follow_redirects=False,
        )
        stats_response = client.get(
            f"{settings.API_V1_STR}/{shorten_response.json().get('shortcode')}/stats"
        )
        assert stats_response.status_code == 200
        content = stats_response.json()
        assert "created" in content
        assert "created" != None
        assert "lastRedirect" in content
        assert "lastRedirect" != None
        assert "redirectCount" in content
        assert content["redirectCount"] == 1

    def test_it_returns_404_when_using_nonexisting_shortcode(
        self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_V1_STR}/doesnotexist/stats")
        assert response.status_code == 404
