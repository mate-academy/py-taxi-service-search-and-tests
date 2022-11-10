from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "NWU12345"
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_number(self):
        form = DriverLicenseUpdateForm({"license_number": "LCN13579"})

        self.assertTrue(form.is_valid())

    def test_correct_entry_license_number(self):
        incorrect_license_number = [
            "AWE1234", "Dfx45678", "ADV56I85", "KL189756"
        ]
        for license_number in incorrect_license_number:
            form = DriverLicenseUpdateForm({"license_number": license_number})

            self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "test.user"}
        form = DriverSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        form_data = {"model": "test model"}
        form = CarSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {"name": "test name"}
        form = ManufacturerSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
