from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "123test123",
            "password2": "123test123",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "TES11123"
        }

    def test_driver_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_wrong_license_number(self):
        license_data = ["TES1234567890",
                        "tes12345",
                        "TEST1234"]
        for data in license_data:
            self.form_data["license_number"] = data
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
