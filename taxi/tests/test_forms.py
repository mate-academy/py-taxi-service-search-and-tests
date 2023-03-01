from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverLicenseUpdateForm
)


class DriverUsernameSearchFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            "username": "A"
        }
        form = DriverUsernameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class CarModelSearchFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            "model": "Corolla"
        }
        form = CarModelSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class ManufacturerNameSearchFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            "name": "Toyota"
        }
        form = ManufacturerNameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class UpdateLicenseForm(TestCase):

    def test_form_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
