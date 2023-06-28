from django.test import TestCase

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    DriverUsernameSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class FormTest(TestCase):
    def test_license_update_form_with_non_valid_data(self):
        form_data = {"license_number": "TS1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_licensenumber_first_last_name_is_valid(
        self,
    ):
        form_data = {
            "username": "username",
            "password1": "passtes45",
            "password2": "passtes45",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "GHJ47896",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form(self):
        form_data = {"username": "testuser"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "Toyota"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {"name": "Ford"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
