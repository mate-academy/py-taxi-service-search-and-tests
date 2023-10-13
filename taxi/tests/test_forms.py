from django.test import TestCase
from django import forms

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchFieldForm,
)
from taxi.models import Car, Manufacturer


class CarFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_to_test = Car.objects.create(
            model="Test_model",
            manufacturer=Manufacturer.objects.create(name="Big", country="UA"),
        )

    def test_drivers_field(self) -> None:
        self.form = CarForm()
        self.assertIsInstance(
            self.form.fields["drivers"].widget, forms.CheckboxSelectMultiple
        )

    def test_valid_data(self) -> None:
        self.form = CarForm(
            data={
                "model": "Tesla",
                "manufacturer": self.car_to_test.manufacturer,
            }
        )
        self.assertTrue(self.form.is_valid())

    def test_invalid_data(self) -> None:
        self.form_model_invalid = CarForm(
            data={"model": "", "manufacturer": self.car_to_test.manufacturer}
        )
        self.form_manufacturer_invalid = CarForm(
            data={"model": "Tesla", "manufacturer": None}
        )
        self.assertFalse(self.form_model_invalid.is_valid())
        self.assertFalse(self.form_manufacturer_invalid.is_valid())


class DriverCreationFormTest(TestCase):
    def test_additional_fields(self) -> None:
        self.form = DriverCreationForm()
        self.assertIn("license_number", self.form.fields)
        self.assertIn("first_name", self.form.fields)
        self.assertIn("last_name", self.form.fields)


class ValidateLicenseNumberTest(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.invalid_lisence_nums = {
            "short": "ABC123",
            "non-digits": "ABCDWXYZ",
            "no-uppercase": "abc12345",
            "last_5_no_digits": "ABC1234G",
        }

    def test_valid_form_data(self):
        form_creation = DriverCreationForm(data={"license_number": "ABC12345"})
        form_update_license_number = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertNotIn("license_number", form_creation.errors)
        self.assertNotIn("license_number", form_update_license_number.errors)

    def test_invalid_license_number_short(self):
        expected_error = ["License number should consist of 8 characters"]
        license_number_value = self.invalid_lisence_nums["short"]
        form_creation = DriverCreationForm(
            data={"license_number": license_number_value}
        )
        form_update_license_number = DriverLicenseUpdateForm(
            data={"license_number": license_number_value}
        )
        self.assertEqual(
            form_creation.errors.get("license_number"), expected_error
        )
        self.assertEqual(
            form_update_license_number.errors.get("license_number"),
            expected_error,
        )

    def test_invalid_license_number_non_uppercase(self):
        expected_error = ["First 3 characters should be uppercase letters"]
        license_number_value = self.invalid_lisence_nums["no-uppercase"]
        form_creation = DriverCreationForm(
            data={"license_number": license_number_value}
        )
        form_update_license_number = DriverLicenseUpdateForm(
            data={"license_number": license_number_value}
        )
        self.assertEqual(
            form_creation.errors.get("license_number"), expected_error
        )
        self.assertEqual(
            form_update_license_number.errors.get("license_number"),
            expected_error,
        )

    def test_invalid_license_number_non_digits(self):
        expected_error = ["Last 5 characters should be digits"]
        license_number_value = self.invalid_lisence_nums["non-digits"]
        form_creation = DriverCreationForm(
            data={"license_number": license_number_value}
        )
        form_update_license_number = DriverLicenseUpdateForm(
            data={"license_number": license_number_value}
        )
        self.assertEqual(
            form_creation.errors.get("license_number"), expected_error
        )
        self.assertEqual(
            form_update_license_number.errors.get("license_number"),
            expected_error,
        )


class SearchFieldFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = SearchFieldForm()
        cls.search_field = cls.form.fields["search_field"]

    def test_max_length(self) -> None:
        self.assertEqual(self.search_field.max_length, 255)

    def test_label(self) -> None:
        self.assertEqual(self.search_field.label, "")

    def test_widget_and_placeholder(self) -> None:
        widget = self.search_field.widget
        self.assertIsInstance(widget, forms.TextInput)
        self.assertEqual(widget.attrs.get("placeholder"), "Search by ")
