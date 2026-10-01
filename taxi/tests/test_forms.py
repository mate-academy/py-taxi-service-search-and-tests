from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    ManufacturerSearchForm,
    DriverSearchForm, CarSearchForm
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation(self):

        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validation_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

        with self.assertRaises(ValidationError):
            validate_license_number("ABc12345")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC124d5")


class DriverSearchFormTest(TestCase):
    def test_name_field_not_required(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_valid_search_query(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")

    def test_name_field_widget_attrs(self):
        form = DriverSearchForm()
        widget = form.fields["username"].widget
        self.assertEqual(form.fields["username"].label, "")
        self.assertEqual(widget.attrs.get("placeholder"), "Search by username")


class ManufacturerSearchFormTest(TestCase):
    def test_name_field_not_required(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_valid_search_query(self):
        form = ManufacturerSearchForm(data={"name": "Audi"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Audi")

    def test_name_exceeds_max_length(self):
        form = ManufacturerSearchForm(data={"name": "a" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_field_widget_attrs(self):
        form = ManufacturerSearchForm()
        widget = form.fields["name"].widget
        self.assertEqual(form.fields["name"].label, "")
        self.assertEqual(widget.attrs.get("placeholder"), "Search by name")


class CarsSearchFormTest(TestCase):
    def test_name_field_not_required(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_valid_search_query(self):
        form = CarSearchForm(data={"model": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test")

    def test_name_field_widget_attrs(self):
        form = CarSearchForm()
        widget = form.fields["model"].widget
        self.assertEqual(form.fields["model"].label, "")
        self.assertEqual(widget.attrs.get("placeholder"), "Search by model")
