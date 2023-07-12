from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    @staticmethod
    def create_form(license_number):
        return DriverLicenseUpdateForm(
            data={
                "license_number": license_number
            }
        )

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_is_valid(self):
        self.assertTrue(self.create_form("ABD12345").is_valid())

    def test_license_number_must_len_not_equal_8(self):
        self.assertFalse(self.create_form("ABCDEF12345").is_valid())
        self.assertFalse(self.create_form("ASC123").is_valid())

    def test_license_number_first_3_letter_must_be_str(self):
        self.assertFalse(self.create_form("ABCD12234").is_valid())

    def test_license_number_last_6_number_must_be_int(self):
        self.assertFalse(self.create_form("ABCD12231231314").is_valid())

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "test"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {
            "model": "Pasat B6"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {
            "username": "test"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
