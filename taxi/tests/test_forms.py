from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class CarsFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="pass12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country",
        )

    def test_car_form_is_valid(self):
        form_data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer,
            "drivers": [self.user],
        }
        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_drivers_field_widget_should_be_checkbox_select_multiple(self):
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"].widget, forms.CheckboxSelectMultiple
        )


class DriversFormsTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_user",
            "license_number": "QWE12345",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password1": "password12345@",
            "password2": "password12345@",
        }
        self.initialize_form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_is_valid(self):
        self.assertTrue(self.initialize_form.is_valid())

    def test_license_number_should_consist_of_8_characters(self):
        self.form_data["license_number"] = "QWER12345"

        self.assertFalse(self.initialize_form.is_valid())
        self.assertEqual(
            self.initialize_form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_license_number_should_have_first_3_uppercase_letters(self):
        self.form_data["license_number"] = "QwE12345"

        self.assertFalse(self.initialize_form.is_valid())
        self.assertEqual(
            self.initialize_form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_license_number_last_5_characters_should_be_digits(self):
        self.form_data["license_number"] = "QWE1234K"

        self.assertFalse(self.initialize_form.is_valid())
        self.assertEqual(
            self.initialize_form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

    def test_driver_license_update_form_is_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
