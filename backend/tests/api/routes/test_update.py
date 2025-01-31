from fastapi.testclient import TestClient

from app.core.config import settings


class TestIntegration:
    def test_it_updates_when_passing_correct_parameters(
        self,
        client: TestClient,
    ) -> None:
        shorten_data = {"url": "https://www.example.com"}
        shorten_response = client.post(
            f"{settings.API_V1_STR}/shorten", json=shorten_data
        )
        update_data = {"url": "https://www.example.org"}
        update_response = client.post(
            f"{settings.API_V1_STR}/update/{shorten_response.json().get('update_id')}",
            json=update_data,
        )
        assert update_response.status_code == 201
        assert shorten_response.json().get("shortcode") == update_response.json().get(
            "shortcode"
        )

    def test_it_returns_400_when_passing_empty_url_parameter(
        self,
        client: TestClient,
    ) -> None:
        shorten_data = {"url": "https://www.example.com"}
        shorten_response = client.post(
            f"{settings.API_V1_STR}/shorten", json=shorten_data
        )
        update_data = {"url": ""}
        update_response = client.post(
            f"{settings.API_V1_STR}/update/{shorten_response.json().get('update_id')}",
            json=update_data,
        )
        assert update_response.status_code == 400

    def test_it_returns_401_when_passing_unknown_update_id(
        self,
        client: TestClient,
    ) -> None:
        update_data = {"url": "https://www.example.org"}
        update_response = client.post(
            f"{settings.API_V1_STR}/update/00000000-0000-0000-0000-000000000000",
            json=update_data,
        )
        assert update_response.status_code == 401

    def test_it_returns_412_when_passing_invalid_url(
        self,
        client: TestClient,
    ) -> None:
        shorten_data = {"url": "https://www.example.com"}
        shorten_response = client.post(
            f"{settings.API_V1_STR}/shorten", json=shorten_data
        )
        update_data = {"url": "https://www.<example>.com"}
        update_response = client.post(
            f"{settings.API_V1_STR}/update/{shorten_response.json().get('update_id')}",
            json=update_data,
        )
        assert update_response.status_code == 412
