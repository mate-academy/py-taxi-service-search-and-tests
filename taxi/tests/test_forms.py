from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchForm,
)

User = get_user_model()


class FormsTests(TestCase):
    def test_driver_creation_form_valid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "badlicense",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "XYZ12",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertTrue(any(
            "License number should consist of 8 characters" in e
            or "Last 5 characters should be digits" in e
            or "First 3 characters should be uppercase letters" in e
            for e in form.errors["license_number"]
        ))

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "DEF67890"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {"license_number": "bad123"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertTrue(any(
            "License number should consist of 8 characters" in e
            or "Last 5 characters should be digits" in e
            or "First 3 characters should be uppercase letters" in e
            for e in form.errors["license_number"]
        ))

    def test_car_form_has_drivers_field(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)
        self.assertEqual(
            form.fields["drivers"].__class__.__name__,
            "ModelMultipleChoiceField"
        )

    def test_search_form_field(self):
        form = SearchForm(data={"search": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "test")
