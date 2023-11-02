from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test_first_name",
            "last_name": "test_second_name",
            "license_number": "ABC98765"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_is_valid(self):
        self.assertFalse(self.license_form("abc98765").is_valid())
        self.assertFalse(self.license_form("ABC987654321").is_valid())
        self.assertTrue(self.license_form("ABC98765").is_valid())

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    @staticmethod
    def license_form(license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": license_number}
        )
