from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, \
    CarModelSearchForm, DriversUsernameSearchForm, ManufacturerNameSearchForm


class DriverTests(TestCase):
    def test_creating_with_license_number_first_last_name_is_valid(self):
        form_data = {"username": "test1",
                     "license_number": "DSS12345",
                     "first_name": "213",
                     "last_name": "213",
                     "password1": "wdaszwdas1234",
                     "password2": "wdaszwdas1234"}
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test1")
        self.assertEqual(form.cleaned_data["license_number"], "DSS12345")
        self.assertEqual(form.cleaned_data["first_name"], "213")
        self.assertEqual(form.cleaned_data["last_name"], "213")

    def test_driver_licence_update_form_with_valid_value(self):
        form_data = {"license_number": "EWQ12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_licence_update_form_with_wrong_value(self):
        form_data = {"license_number": "EWQ1234D"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_username_search_form_empty(self):
        form = DriversUsernameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_username_search_form_with_value(self):
        form = DriversUsernameSearchForm(data={"username": "admin"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "admin")

    def test_driver_username_search_form_too_long(self):
        form = DriversUsernameSearchForm(data={"username": "user" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CarTests(TestCase):
    def test_car_model_search_form_empty(self):
        form = CarModelSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_model_search_form_with_value(self):
        form = CarModelSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")

    def test_car_model_search_form_too_long(self):
        form = CarModelSearchForm(data={"model": "a" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class ManufacturerTests(TestCase):
    def test_manufacturer_name_search_form_empty(self):
        form = ManufacturerNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_name_search_form_with_value(self):
        form = ManufacturerNameSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BMW")

    def test_manufacturer_name_search_form_too_long(self):
        form = ManufacturerNameSearchForm(data={"name": "a" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
