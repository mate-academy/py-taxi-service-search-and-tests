from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    CarSearchForm
)
from django import forms
from taxi.models import Manufacturer


class FormsTests(TestCase):
    def test_car_form(self):
        form = CarForm(
            data={
                "manufacturer": Manufacturer.objects.create(
                    name="Test manufacturer"
                ),
                "model": "Test model",
                "year": 2021,
                "drivers": [get_user_model().objects.create(
                    username="test_user"
                )
                ],
            }
        )
        self.assertTrue(form.is_valid())
        self.assertIsInstance(
            form.fields["drivers"],
            forms.ModelMultipleChoiceField
        )
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )
        self.assertEqual(
            form.cleaned_data,
            form.cleaned_data
        )

    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ADB12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            {"license_number": "ABC12345"}
        )


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        license_number = "ABC12345"
        result = validate_license_number(license_number)
        self.assertEqual(result, license_number)

    def test_invalid_length(self):
        license_number = "ABC123"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_invalid_letters(self):
        license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_invalid_digits(self):
        license_number = "ABCabcde"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)


class SearchFormTest(TestCase):
    def test_search_form(self):
        form_car = CarSearchForm(
            data={"title": "Test car"}
        )
        form_driver = CarSearchForm(
            data={"title": "Test driver"}
        )
        form_manufacturer = CarSearchForm(
            data={"title": "Test manufacturer"}
        )
        self.assertTrue(form_manufacturer.is_valid())
        self.assertTrue(form_driver.is_valid())
        self.assertTrue(form_car.is_valid())
        self.assertEqual(
            form_manufacturer.cleaned_data,
            {"title": "Test manufacturer"}
        )
        self.assertEqual(
            form_driver.cleaned_data,
            {"title": "Test driver"}
        )
        self.assertEqual(
            form_car.cleaned_data,
            {"title": "Test car"}
        )
