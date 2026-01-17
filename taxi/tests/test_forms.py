from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)


class TestDriverCreationForm(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "test_user",
            "password1": "Gfhjkmjlby@",
            "password2": "Gfhjkmjlby@",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestDriverLicenseUpdateForm(TestCase):
    def test_valid_form(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestDriverUsernameSearchForm(TestCase):
    def test_valid_form(self):
        form = DriverUsernameSearchForm(data={"username": "test user"})
        self.assertTrue(form.is_valid())


class TestCarModelSearchForm(TestCase):
    def test_valid_form(self):
        form = CarModelSearchForm(data={"model": "test model"})
        self.assertTrue(form.is_valid())


class TestManufacturerNameSearchForm(TestCase):
    def test_valid_form(self):
        form = ManufacturerNameSearchForm(data={"name": "test name"})
        self.assertTrue(form.is_valid())
