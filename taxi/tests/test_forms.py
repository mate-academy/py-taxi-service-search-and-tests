import pytest
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    @pytest.mark.parametrize("license_number, result", [
        ("111", False),
        ("aaa", False),
        ("aaa11111", False),
        ("aaaaaaaa", False),
        ("AAA11111", True),
    ])
    def test_license_number_is_valid(self, license_number, result):
        form_data = {
            "username": "driver",
            "password1": "NotCommonPassword123",
            "password2": "NotCommonPassword123",
            "first_name": "TestName",
            "last_name": "Last_name",
            "license_number": license_number,
        }
        form = DriverCreationForm(data=form_data)
        print(form.is_valid())
        assert form.is_valid() == result
