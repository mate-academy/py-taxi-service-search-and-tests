from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm,
)

from taxi.models import Driver, Car, Manufacturer


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        test_data = {
            "username": "test_username",
            "password1": "password_test",
            "password2": "password_test",
            "license_number": "AAA11111",
            "first_name": "test_first",
            "last_name": "test_last"
        }
        form = DriverCreationForm(data=test_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_is_valid(self):
        test_data = {
            "license_number": "AAA11111"
        }
        form = DriverLicenseUpdateForm(data=test_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)

    def test_driver_license_update_not_is_valid(self):
        test_data = {
            "license_number": "AAA1111"
        }
        form = DriverLicenseUpdateForm(data=test_data)
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def test_driver_search_is_valid(self):
        test_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_car_search_is_valid(self):
        test_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_is_valid(self):
        test_data = {
            "name": "test_name",
        }
        form = ManufacturerSearchForm(data=test_data)
        self.assertTrue(form.is_valid())
