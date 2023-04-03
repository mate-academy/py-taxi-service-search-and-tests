from django.test import TestCase
from django import forms

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "GTE78986",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_form_fields(self):
        form = DriverLicenseUpdateForm()
        expected_fields = ["license_number"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_clean_license_number_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_clean_license_number_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_clean_license_number_too_long(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345A"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_clean_license_number_invalid_first_three_chars(self):
        form = DriverLicenseUpdateForm(data={"license_number": "Abc12345"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_clean_license_number_invalid_last_five_chars(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234A"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTest(TestCase):
    def test_form_fields(self):
        form = DriverSearchForm()
        expected_fields = ["username"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_username_widget(self):
        form = DriverSearchForm()
        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)


class CarSearchFormTest(TestCase):
    def test_form_fields(self):
        form = CarSearchForm()
        expected_fields = ["model"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_model_widget(self):
        form = CarSearchForm()
        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)


class ManufacturerSearchFormTest(TestCase):
    def test_form_fields(self):
        form = ManufacturerSearchForm()
        expected_fields = ["name"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_name_widget(self):
        form = ManufacturerSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
