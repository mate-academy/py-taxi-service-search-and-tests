from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class FormTests(TestCase):
    def test_driver_creation_form_fields_and_model(self):
        form = DriverCreationForm()
        self.assertEqual(form._meta.model, get_user_model())
        self.assertIn("license_number", form.fields)

    def test_driver_license_update_form_fields_and_model(self):
        form = DriverLicenseUpdateForm()
        self.assertEqual(form._meta.model, get_user_model())
        self.assertEqual(list(form.fields.keys()), ["license_number"])

    def test_driver_license_number_validation_invalid(self):
        invalid_scenarios = [
            ("12345678", "First 3 characters should be uppercase letters"),
            ("ABCDE", "License number should consist of 8 characters"),
            ("ABC123DE", "Last 5 characters should be digits"),
        ]

        for license_num, error_msg in invalid_scenarios:
            with self.subTest(license_number=license_num):
                form = DriverLicenseUpdateForm(
                    data={"license_number": license_num}
                )
                self.assertFalse(form.is_valid())
                self.assertIn(error_msg, form.errors["license_number"])

    def test_car_form_drivers_field_widget(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_search_forms_are_not_required(self):
        self.assertTrue(DriverSearchForm(data={}).is_valid())
        self.assertTrue(CarSearchForm(data={}).is_valid())
        self.assertTrue(ManufacturerSearchForm(data={}).is_valid())
