import unittest

from fastapi.testclient import TestClient

from app.api.routes.shorten import (
    RANDOM_SHORTCODE_CHARS,
    generate_random_shortcode,
    validate_shortcode,
)
from app.core.config import settings


class TestIntegration:
    def test_it_creates_with_random_shortcode_when_passing_no_shortcode_parameter(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com"}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 201
        content = response.json()
        assert "shortcode" in content
        assert "update_id" in content

    def test_it_creates_with_random_shortcode_when_passing_empty_shortcode_parameter(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com", "shortcode": ""}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 201
        content = response.json()
        assert "shortcode" in content
        assert "update_id" in content

    def test_it_creates_with_custom_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com", "shortcode": "pytest2"}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 201
        content = response.json()
        assert "shortcode" in content
        assert "update_id" in content

    def test_it_returns_400_when_passing_empty_url_parameter(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": ""}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 400

    def test_it_returns_409_when_using_existing_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com", "shortcode": "pytest"}
        client.post(f"{settings.API_V1_STR}/shorten", json=data)
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 409

    def test_it_returns_412_when_using_invalid_url(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.<example>.com"}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 412

    def test_it_returns_412_when_using_invalid_shortcode(
        self,
        client: TestClient,
    ) -> None:
        data = {"url": "https://www.example.com", "shortcode": "<shortcode>"}
        response = client.post(f"{settings.API_V1_STR}/shorten", json=data)
        assert response.status_code == 412


class TestGenerateRandomShortcode(unittest.TestCase):
    def test_it_generates_with_correct_length(self) -> None:
        shortcode = generate_random_shortcode()
        self.assertEqual(len(shortcode), 6)

    def test_it_generates_with_only_allowed_characters(self) -> None:
        shortcode = generate_random_shortcode()
        for char in shortcode:
            self.assertIn(
                char,
                RANDOM_SHORTCODE_CHARS,
            )

    def test_it_generates_a_string(self) -> None:
        shortcode = generate_random_shortcode()
        self.assertIsInstance(shortcode, str)


class TestValidateShortcode(unittest.TestCase):
    def test_it_validates_correct_shortcodes(self) -> None:
        valid_shortcodes = [
            "abc",
            "A1b2C3",
            "a-b_c.d~E",
            "Z",
            "0",
            "1234567890",
            "-._~",
            "a.b-c_d~E",
            "testShortCode123",
            "valid_shortcode-.~",
        ]

        for shortcode in valid_shortcodes:
            with self.subTest(shortcode=shortcode):
                result = validate_shortcode(shortcode)
                self.assertEqual(result, shortcode)

    def test_it_invalidates_incorrect_shortcodes(self) -> None:
        invalid_shortcodes = [
            "abc!",  # Contains '!'
            "hello/world",  # Contains '/'
            "space ",  # Contains space
            "",  # Empty string
            "a@b#c",  # Contains '@' and '#'
            "test\n",  # Contains newline character
            "😊",  # Contains emoji
            "tab\t",  # Contains tab character
            "foo/bar",  # Contains '/'
            "percent%",  # Contains '%'
            "semi;colon",  # Contains ';'
            "colon:",  # Contains ':'
            "question?",  # Contains '?'
            "slash\\",  # Contains backslash
            "pipe|",  # Contains '|'
            "brace{",  # Contains '{'
            "bracket[",  # Contains '['
            "angle<",  # Contains '<'
            "greater>",  # Contains '>',
        ]

        for shortcode in invalid_shortcodes:
            with self.subTest(shortcode=shortcode):
                with self.assertRaises(ValueError):
                    validate_shortcode(shortcode)
