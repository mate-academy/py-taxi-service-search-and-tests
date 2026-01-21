from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, validate_license_number


class CarFormTest(TestCase):
    def test_widget_check_box_is_select_multiple(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget, forms.CheckboxSelectMultiple
        )

    def test_drivers_field_is_model_multiple_choice_field(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"], forms.ModelMultipleChoiceField
        )


class DriverCreationFormTests(TestCase):
    def test_driver_form(self):
        form_data = {
            "username": "testdriver",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testdriver")
        self.assertEqual(form.cleaned_data["first_name"], "John")
        self.assertEqual(form.cleaned_data["last_name"], "Doe")
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_driver_license_number_len(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")
        with self.assertRaises(ValidationError):
            validate_license_number("AB123")
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")
