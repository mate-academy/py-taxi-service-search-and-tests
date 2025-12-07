from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerNameSearchForm,
    CarModelSearchForm,
    DriverUsernameSearchForm
)


class DriverFormsTests(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "SSD12345"
        }

    def test_driver_creation_with_license_first_name_last_name_is_valid(self):
        form = DriverCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)
        self.assertEqual(form.cleaned_data.get("license_number"), "SSD12345")

    def get_form(self, **kwargs):
        form_data = self.valid_form_data.copy()
        form_data.update(kwargs)
        return DriverCreationForm(data=form_data)

    def test_clean_license_number_valid(self):
        form = self.get_form(license_number="ABC12345")
        self.assertTrue(form.is_valid())

    def test_clean_license_number_invalid(self):
        form = self.get_form(license_number="123")
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_clean_license_number_invalid_chars(self):
        form = self.get_form(license_number="ABCD@123")
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)


class SearchFormsTests(TestCase):

    def test_driver_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search_form_valid(self):
        form_data = {"model": "testmodel"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "testmodel")

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "testname"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "testname")

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
