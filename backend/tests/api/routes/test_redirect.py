from fastapi.testclient import TestClient

from app.core.config import settings


class TestIntegration:
    def test_it_redirects_when_using_existing_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com"}
        shorten_response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        redirect_response = client.get(
            f"{settings.API_V1_STR}/{shorten_response.json().get('shortcode')}",
            follow_redirects=False,
        )
        assert redirect_response.status_code == 302
        assert redirect_response.headers["Location"] == data["url"]

    def test_it_returns_404_when_using_nonexisting_shortcode(
        self,
        client: TestClient,
    ) -> None:
        redirect_response = client.get(
            f"{settings.API_V1_STR}/doesnotexist",
            follow_redirects=False,
        )
        assert redirect_response.status_code == 404
