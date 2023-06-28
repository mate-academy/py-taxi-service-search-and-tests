from django.test import TestCase

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormTest(TestCase):
    def test_license_update_form_with_non_valid_data(self):
        form_data = {"license_number": "TS1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form(
        self,
    ):
        form_data = {
            "username": "user_name",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "test first name",
            "last_name": "test last name",
            "license_number": "CCE12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "Mazda"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
