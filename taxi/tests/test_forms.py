from django.test import TestCase
from taxi.forms import (ManufacturerSearchForm, CarSearchForm,
                        DriverSearchForm, DriverLicenseUpdateForm)


class SearchFormTestCase(TestCase):

    def test_search_form(self):
        form_manufacturer = {
            "name": "Test Name"
        }
        form = ManufacturerSearchForm(data=form_manufacturer)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_manufacturer)

        form_car = {
            "model": "Test Model"
        }
        form = CarSearchForm(data=form_car)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_car)

        form_driver = {
            "username": "Test Username"
        }
        form = DriverSearchForm(data=form_driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_driver)

    def test_validate_license_number(self):
        form_license_number = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_license_number)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_license_number)
