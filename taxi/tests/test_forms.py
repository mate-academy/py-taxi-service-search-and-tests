from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from django.test import TestCase


class DriverCreationFormTests(TestCase):

    def setUp(self):
        self.valid_form_data = {
            "username": "testdriver",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "ABC12345"
        }

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
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_form_widget(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_car_search_form_valid(self):
        form_data = {"model": "testmodel"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "testmodel")

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_form_widget(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "testname"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "testname")

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_form_widget(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )
