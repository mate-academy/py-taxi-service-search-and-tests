from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class DriverCreationFormTest(TestCase):

    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "test123",
            "password1": "password123test",
            "password2": "password123test",
            "first_name": "user_test",
            "last_name": "test_user",
            "license_number": "ADM56984"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


class ManufacturerSearchFormTests(TestCase):

    def test_blank_form(self):
        form_data = {}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_widgets_attributes(self):
        form = ManufacturerSearchForm()

        self.assertIn('placeholder="Search by name"', str(form))


class CarSearchFormTests(TestCase):

    def test_blank_form(self):
        form_data = {}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_widgets_attributes(self):
        form = CarSearchForm()

        self.assertIn('placeholder="Search be model"', str(form))


class DriverSearchFormTests(TestCase):

    def test_blank_form(self):
        form_data = {}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_widgets_attributes(self):
        form = DriverSearchForm()

        self.assertIn('placeholder="Search by username', str(form))


class ValidationLicenseNuberTests(TestCase):

    def test_validation_error__when_number_of_characters_more_then_8(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ADM569844")

    def test_validation_error_when_first_3_characters_not_in_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("adM56984")

    def test_validation_error_when_last_5_characters_not_is_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ADM569sd")
