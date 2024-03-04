from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, DriverUsernameSearchForm, CarModelSearchForm, \
    ManufacturerNameSearchForm


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test",
            "last_name": "Test",
        }

    def test_create_when_license_number_is_valid(self):
        self.form_data["license_number"] = "QWE12345"
        form = DriverCreationForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_when_license_number_is_invalid(self):
        for license_number in ("QwE12345", "QWE123456", "QWERTYUI"):
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
            

class DriverLicenseUpdateFormTest(TestCase):
    def test_update_when_license_number_is_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "QWE12345"})
        self.assertTrue(form.is_valid())

    def test_update_when_license_number_is_invalid(self):
        for license_number in ("QwE12345", "QWE123456", "QWERTYUI"):
            form = DriverLicenseUpdateForm(
                data={"license_number": license_number}
            )
            self.assertFalse(form.is_valid())


class SearchFormsTest(TestCase):
    def test_driver_username_search_form(self):
        form = DriverUsernameSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")

    def test_car_model_search_form(self):
        form = CarModelSearchForm(data={"model": "Tesla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Tesla")

    def test_manufacturer_name_search_form(self):
        form = ManufacturerNameSearchForm(data={"name": "TESLA"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "TESLA")
