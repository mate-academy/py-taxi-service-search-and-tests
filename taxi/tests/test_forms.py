import pytest
from parameterized import parameterized
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    @parameterized.expand([
        ("111", False),
        ("aaa", False),
        ("aaa11111", False),
        ("aaaaaaaa", False),
        ("AAA11111", True),
    ])
    def test_license_number_is_valid(self, license_number, expected_result):
        form_data = {
            "username": "driver",
            "password1": "NotCommonPassword123",
            "password2": "NotCommonPassword123",
            "first_name": "TestName",
            "last_name": "Last_name",
            "license_number": license_number,
        }
        form = DriverCreationForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.is_valid(), expected_result)
