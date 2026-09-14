from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_license_validation(self):
        valid_data = {
            "username": "driver1",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "AAA12345",
            "password1": "ComplexP@ssw0rd123",
            "password2": "ComplexP@ssw0rd123",
        }

        form = DriverCreationForm(data=valid_data)
        self.assertTrue(form.is_valid())

        invalid_data_short = valid_data.copy()
        invalid_data_short["license_number"] = "AA12345"
        self.assertFalse(DriverCreationForm(
            data=invalid_data_short).is_valid()
        )

        invalid_data_starts_num = valid_data.copy()
        invalid_data_starts_num["license_number"] = "123AAAAA"
        self.assertFalse(DriverCreationForm(
            data=invalid_data_starts_num).is_valid()
        )

        invalid_data_ends_letters = valid_data.copy()
        invalid_data_ends_letters["license_number"] = "AAAAA123"
        self.assertFalse(DriverCreationForm(
            data=invalid_data_ends_letters).is_valid()
        )
