from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    validate_license_number,
)


class ManufacturerSearchFormTest(TestCase):
    def test_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_form_empty_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_form_label_empty(self):
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_form_is_too_long(self):
        form = ManufacturerSearchForm(data={"name": "A" * 256})
        self.assertFalse(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_form_valid(self):
        form = CarSearchForm(data={"model": "MX-5"})
        self.assertTrue(form.is_valid())

    def test_form_empty_valid(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_form_label_empty(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].label, "")

    def test_form_is_too_long(self):
        form = CarSearchForm(data={"model": "A" * 256})
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_form_valid(self):
        form = DriverSearchForm(data={"username": "MX-5"})
        self.assertTrue(form.is_valid())

    def test_form_empty_valid(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_form_is_too_long(self):
        form = DriverSearchForm(data={"username": "A" * 256})
        self.assertFalse(form.is_valid())

    def test_form_label_empty(self):
        form = DriverSearchForm()
        self.assertEqual(form.fields["username"].label, "")


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_first_three_letter_is_not_alpha(self):
        with self.assertRaises(ValidationError):
            validate_license_number("12345678")

    def test_first_three_letter_is_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc123456")

    def test_last_five_character_is_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCD1234")
