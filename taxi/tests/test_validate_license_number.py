import pytest
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number


def test_validate_license_number():
    assert validate_license_number("AAA12345") == "AAA12345"


def test_validate_license_number_invalid_length():
    with pytest.raises(
            ValidationError,
            match="License number should consist of 8 characters"
    ):
        validate_license_number("AA12345")


def test_validate_license_number_invalid_first_3_characters():
    with pytest.raises(
            ValidationError,
            match="First 3 characters should be uppercase letters"
    ):
        validate_license_number("AAa12345")


def test_validate_license_number_invalid_last_5_digits():
    with pytest.raises(
            ValidationError,
            match="Last 5 characters should be digits"
    ):
        validate_license_number("AAA1234A")
