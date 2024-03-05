from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="strong_password"
        )
        self.form_data = {
            "username": "King_of_the_tests",
            "password1": "secret_password1984#",
            "password2": "secret_password1984#",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "license_number": "TNT54321",
        }

    def test_user_creation_with_customs_fields(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_user_creation_with_invalid_license_number(self):
        invalid_license_numbers = [
            "RIP1234",
            "tTT12345",
            "TT123456",
            " "
        ]
        for invalid_license in invalid_license_numbers:
            self.form_data["license_number"] = invalid_license
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())

    def test_update_license_number(self):
        new_license_form = {
            "license_number": "UAE12345",
        }
        form = DriverLicenseUpdateForm(data=new_license_form)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, new_license_form)

    def test_driver_search_form(self):
        form = DriverSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"], self.form_data["username"]
        )

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Benderomobil"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Benderomobil")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "test_concern"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_concern")
