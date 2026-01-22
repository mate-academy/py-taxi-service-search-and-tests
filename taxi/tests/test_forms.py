from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Car

Driver = get_user_model()


class CarFormTest(TestCase):
    def test_car_form_model(self):
        form = CarForm()
        self.assertEqual(form._meta.model, Car)

    def test_car_form_fields(self):
        form = CarForm()
        self.assertEqual(
            list(form.fields.keys()),
            ["model", "manufacturer", "drivers"]
        )

    def test_car_form_drivers(self):
        form = CarForm()
        self.assertEqual(form.fields["drivers"].label, None)

        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

        self.assertEqual(
            str(form.fields["drivers"].queryset.query),
            str(Driver.objects.all().query)
        )


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_subclass(self):
        self.assertTrue(issubclass(DriverCreationForm, UserCreationForm))

    def test_driver_creation_form_form_meta_is_subclass(self):
        self.assertTrue(
            issubclass(DriverCreationForm.Meta, UserCreationForm.Meta)
        )

    def test_driver_creation_form_model(self):
        form = DriverCreationForm()
        self.assertEqual(form._meta.model, Driver)

    def test_driver_creation_form_fields(self):
        form = DriverCreationForm()
        self.assertEqual(
            tuple(form.fields.keys()),
            UserCreationForm.Meta.fields + (
                "license_number",
                "first_name",
                "last_name",
                "password1",
                "password2"
            )
        )

    def test_license_number_required(self):
        form_data = {
            "username": "testuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "license_number": ""
        }

        form = DriverCreationForm(
            data=form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["This field is required."]
        )

    def test_license_number_validates_length_not_8(self):
        form_data = {
            "username": "testuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "license_number": "1234"
        }

        form = DriverCreationForm(
            data=form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

        form_data["license_number"] = "123456789"
        form = DriverCreationForm(
            data=form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_license_number_validates_first_3_is_not_uppercase_letters(self):
        form_data = {
            "username": "testuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "license_number": "aaa12345"
        }

        form = DriverCreationForm(
            data=form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

        form_data["license_number"] = "AA12345"

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_license_number_validates_last_5_is_not_digits(self):
        form_data = {
            "username": "testuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "license_number": "AAAA2345"
        }

        form = DriverCreationForm(
            data=form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

        form_data["license_number"] = "AA1234A"

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

        form_data["license_number"] = "AAA12A45"

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

    def test_license_number_allow_correct(self):
        form_data = {
            "username": "testuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "license_number": "AAA12345"
        }
        form = DriverCreationForm(data=form_data)

        form.is_valid()
        self.assertNotIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_model(self):
        form = DriverLicenseUpdateForm()
        self.assertEqual(form._meta.model, Driver)

    def test_driver_license_update_form_fields(self):
        self.assertEqual(
            DriverLicenseUpdateForm.Meta.fields,
            ["license_number"]
        )

    def test_driver_license_update_form_validations(self):
        form_data = {
            "license_number": ""
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["This field is required."]
        )

        form_data["license_number"] = "1"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

        form_data["license_number"] = "123456789"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

        form_data["license_number"] = "aa123456"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

        form_data["license_number"] = "AAa12345"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

        form_data["license_number"] = "AAA12A45"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

        form_data["license_number"] = "AAA1234A"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

        form_data["license_number"] = "AAA12345"
        form = DriverLicenseUpdateForm(data=form_data)
        form.is_valid()
        self.assertNotIn("license_form", form.errors)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_has_username_field(self):
        form = DriverSearchForm()
        self.assertIn("username", form.fields)

    def test_driver_search_form_username_field(self):
        form = DriverSearchForm()
        username_field = form.fields["username"]

        self.assertIsInstance(username_field, forms.CharField)
        self.assertEqual(username_field.max_length, 255)
        self.assertEqual(username_field.label, "")
        self.assertIsInstance(
            username_field.widget,
            forms.TextInput
        )
        self.assertEqual(
            username_field.widget.attrs["placeholder"],
            "Search by username"
        )


class CarSearchFormTest(TestCase):
    def test_car_search_form_has_model_field(self):
        form = CarSearchForm()
        self.assertIn("model", form.fields)

    def test_car_search_form_model_field(self):
        form = CarSearchForm()
        model_field = form.fields["model"]

        self.assertIsInstance(model_field, forms.CharField)
        self.assertEqual(model_field.max_length, 255)
        self.assertEqual(model_field.label, "")
        self.assertIsInstance(
            model_field.widget,
            forms.TextInput
        )
        self.assertEqual(
            model_field.widget.attrs["placeholder"],
            "Search by model"
        )


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_has_name_field(self):
        form = ManufacturerSearchForm()
        self.assertIn("name", form.fields)

    def test_manufacturer_search_form_name_field(self):
        form = ManufacturerSearchForm()
        name_field = form.fields["name"]

        self.assertIsInstance(name_field, forms.CharField)
        self.assertEqual(name_field.max_length, 255)
        self.assertEqual(name_field.label, "")
        self.assertIsInstance(
            name_field.widget,
            forms.TextInput
        )
        self.assertEqual(
            name_field.widget.attrs["placeholder"],
            "Search by name"
        )
