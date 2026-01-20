# flake8: ignore=E501

from django.forms import CheckboxSelectMultiple
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class TestCarForms(TestCase):
    def test_car_form_uses_checkbox_widget(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            CheckboxSelectMultiple
        )

    def test_car_search_form_has_placeholder(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs.get("placeholder"),
            "Search by model"
        )


class TestDriverForms(TestCase):
    def test_driver_license_update_form_validation_valid_data(self):
        form_data = {"license_number": "TST12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_validation_invalid_data(self):
        invalid_data = {
            "TST1234": "License number should consist of 8 characters",
            "TST123456": "License number should consist of 8 characters",
            "tst12345": "First 3 characters should be uppercase letters",
            "TSTTSTTS": "Last 5 characters should be digits",
        }
        for data, error in invalid_data.items():
            form_data = {"license_number": data}
            form = DriverLicenseUpdateForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors["license_number"], [error])

    def test_driver_search_form_has_placeholder(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs.get("placeholder"),
            "Search by username",
        )


class TestManufacturerForms(TestCase):
    def test_manufacturer_search_form_has_placeholder(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Search by name"
        )
