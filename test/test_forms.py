import pytest
from django.test import TestCase
from parameterized import parameterized

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "test_name",
            "license_number": "NNN12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",
        }

    def create_form_with_data(self, form_data):
        form = DriverCreationForm(data=form_data)
        return form

    @pytest.mark.parametrize(
        "invalid_license_number",
        [
            "NNN1234",
            "aQN12342",
            "QW12342",
        ],
    )
    def test_create_driver_form_with_valid_data(self):
        form = self.create_form_with_data(self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)

    @parameterized.expand([
        ("NNN1234",),
        ("aQN12342",),
        ("QW12342",),
    ])
    def test_create_driver_invalid_license_num(self, invalid_license_number):
        self.valid_form_data["license_number"] = invalid_license_number
        form = self.create_form_with_data(self.valid_form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.valid_form_data)
