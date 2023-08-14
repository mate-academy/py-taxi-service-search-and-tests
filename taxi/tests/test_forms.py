from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "first_name": "test First",
            "last_name": "test Last",
            "username": "test_username",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "ABC12345"
        }

    def test_driver_creation_form_with_firs_last_name_license_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_license_number_change(self):
        modified_form_data = self.form_data.copy()
        modified_form_data["license_number"] = "XYZ987654"

        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters",
        ):
            form = DriverCreationForm(data=modified_form_data)
            form.is_valid()
            form.clean_license_number()
