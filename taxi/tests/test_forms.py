from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm, CarSearchForm)


class FormTests(TestCase):
    def test_driver_creation_form_with_driver_license(self):
        form_data = {
            "username": "user_check",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Test_first",
            "last_name": "Test last",
            "license_number": "ULK12121"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_driver_license(self):
        data_7char = {
            "license_number": "ULK1221"
        }
        data_lower = {
            "license_number": "UlK12121"
        }
        data_2letter = {
            "license_number": "UL212121"
        }
        data_4digits = {
            "license_number": "ULLM2121"
        }
        data_form = {
            "license_number": "ULL12121"
        }

        form_7char = DriverLicenseUpdateForm(data=data_7char)
        form_lower = DriverLicenseUpdateForm(data=data_lower)
        form_2letter = DriverLicenseUpdateForm(data=data_2letter)
        form_4digits = DriverLicenseUpdateForm(data=data_4digits)
        form = DriverLicenseUpdateForm(data=data_form)

        self.assertFalse(form_7char.is_valid())
        self.assertFalse(form_lower.is_valid())
        self.assertFalse(form_2letter.is_valid())
        self.assertFalse(form_4digits.is_valid())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data_form)

    def test_car_search_form(self):
        data_form = {
            "name": "b"
        }

        form = CarSearchForm(data=data_form)
        self.assertTrue(form.is_valid())
