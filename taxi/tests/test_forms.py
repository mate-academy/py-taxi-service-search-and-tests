from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)


class FormsTest(TestCase):
    def test_driver_creation_form_with_firstname_lastname_license_number(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_name",
            "last_name": "test_surname",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_form_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            "license_number": "A1B2C3D4",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_search_form(self):
        form = CarSearchForm(
            data={
                "model": "test"
            }
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(
            data={
                "name": "Test"
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm(
            data={
                "username": "test_username"
            }
        )
        self.assertTrue(form.is_valid())
