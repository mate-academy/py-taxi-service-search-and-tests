from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.driver_data = {
            "username": "testdriver",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "testfirst",
            "last_name": "testlast",
            "license_number": "TTT11111"
        }

    def test_create_license_number_is_valid(self):
        driver_form = DriverCreationForm(self.driver_data)
        self.assertTrue(driver_form.is_valid())
        self.assertEqual(driver_form.cleaned_data, self.driver_data)

    def test_create_license_number_is_not_valid(self):
        wrong_license = self.driver_data.copy()
        wrong_license["license_number"] = "1T2E3S4T"
        driver_form = DriverCreationForm(wrong_license)
        self.assertFalse(driver_form.is_valid())
