import unittest

from app.utils import validate_url


class TestValidateURL(unittest.TestCase):
    def test_it_validates_correct_url(self) -> None:
        valid_url = "http://example.com"
        result = validate_url(valid_url)
        self.assertEqual(result, None)

    def test_it_invalidates_incorrect_url(self) -> None:
        invalid_url = "<example.com>"
        with self.assertRaises(ValueError):
            validate_url(invalid_url)
