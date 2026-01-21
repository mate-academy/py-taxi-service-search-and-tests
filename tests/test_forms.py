from django.forms import CheckboxSelectMultiple
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarForm,
    CarSearchForm,
    DriverLicenseUpdateForm,
    DriverSearchForm
)


class TestManufacturerForms(TestCase):
    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Search by name"
        )


class TestCarForm(TestCase):
    def test_car_form(self):
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"].widget,
            CheckboxSelectMultiple
        )

    def test_car_search_form(self):
        form = CarSearchForm()

        self.assertEqual(
            form.fields["model"].widget.attrs.get("placeholder"),
            "Search by model"
        )


class TestDriverForms(TestCase):
    def test_driver_update_form(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            "ABC12345"
        )

    def test_driver_search_form(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs.get("placeholder"),
            "Search by username"
        )
