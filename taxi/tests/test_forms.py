from django.forms import CheckboxSelectMultiple
from django.forms.widgets import TextInput
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchModelForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchUsernameForm,
    ManufacturerSearchNameForm
)


class CarFormTest(TestCase):

    def test_field_driver_and_widget_in_form(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)
        self.assertIsInstance(
            form.fields["drivers"].widget, CheckboxSelectMultiple
        )

    def test_search_car_form(self):
        form = CarSearchModelForm()
        self.assertIn("model", form.fields)
        self.assertIsInstance(form.fields["model"].widget, TextInput)

        widget = form.fields["model"].widget
        self.assertIn("placeholder", widget.attrs)
        self.assertEqual(widget.attrs["placeholder"], "Search by model")


class DriverFormTest(TestCase):

    def test_field_model_license_number_fires_last_name(self):

        form_data = {
            "username": "john_test",
            "password1": "test123Storng",
            "password2": "test123Storng",
            "license_number": "FFF00000",
            "first_name": "John",
            "last_name": "Carter"
        }
        form = DriverCreationForm(data=form_data)
        print(form.errors)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )

    def test_search_driver_form(self):
        form = DriverSearchUsernameForm()
        self.assertIn("username", form.fields)
        self.assertIsInstance(form.fields["username"].widget, TextInput)

        widget = form.fields["username"].widget
        self.assertIn("placeholder", widget.attrs)
        self.assertEqual(widget.attrs["placeholder"], "Search by username")


class ValidatorLicenseNumberTest(TestCase):
    def test_wrong_len(self):

        data = {"license_number": "FFF00"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFormError(
            form, "license_number",
            "License number should consist of 8 characters"
        )

    def test_wrong_uppercase_liters(self):

        data = {"license_number": "fff00000"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFormError(
            form, "license_number",
            "First 3 characters should be uppercase letters"
        )

    def test_wrong_last_five_characters(self):
        data = {"license_number": "FFF0f0f0"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFormError(
            form, "license_number",
            "Last 5 characters should be digits"
        )


class ManufacturerFormTest(TestCase):

    def test_search_driver_form(self):
        form = ManufacturerSearchNameForm()
        self.assertIn("name", form.fields)
        self.assertIsInstance(form.fields["name"].widget, TextInput)

        widget = form.fields["name"].widget
        self.assertIn("placeholder", widget.attrs)
        self.assertEqual(widget.attrs["placeholder"], "Search by name")
