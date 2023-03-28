from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTests(TestCase):
    def setUp(self):
        self.driver_data = {
            "username": "new_driver",
            "password1": "qWertY9876543",
            "password2": "qWertY9876543",
            "first_name": "Test",
            "last_name": "Testovych",
            "license_number": "AAA12345"
        }

    def test_creation_form_is_valid(self):
        driver_form = DriverCreationForm(self.driver_data)
        self.assertTrue(driver_form.is_valid())
        self.assertEqual(driver_form.cleaned_data, self.driver_data)

    def test_creation_form_is_not_valid(self):
        not_valid_data = self.driver_data.copy()
        not_valid_data["license_number"] = "8790yuikj"
        driver_form = DriverCreationForm(not_valid_data)
        self.assertFalse(driver_form.is_valid())
