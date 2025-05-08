from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)

from taxi.forms import validate_license_number


class TestDriverCreationForm(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_valid_data(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(
            self.form.cleaned_data.get("username"),
            self.form_data.get("username")
        )
        self.assertEqual(
            self.form.cleaned_data.get("first_name"),
            self.form_data.get("first_name")
        )
        self.assertEqual(
            self.form.cleaned_data.get("last_name"),
            self.form_data.get("last_name")
        )
        self.assertEqual(
            self.form.cleaned_data.get("license_number"),
            self.form_data.get("license_number")
        )

    def test_is_license_number_valid(self):
        self.form.is_valid()
        self.assertTrue(
            validate_license_number(
                self.form.cleaned_data["license_number"])
        )

    def test_is_license_number_invalid(self):
        self.form_data["license_number"] = "tes12345"
        self.form = DriverCreationForm(data=self.form_data)
        is_valid = self.form.is_valid()
        self.assertFalse(is_valid)
        with self.assertRaises(ValidationError) as context:
            validate_license_number(self.form_data["license_number"])
        self.assertEqual(
            str(context.exception.messages[0]),
            "License number must consist of exactly three "
            "uppercase letters followed by five digits."
        )


class TestDriverSearchForm(TestCase):
    def setUp(self) -> None:
        self.form = DriverSearchForm()

    def test_driver_search_form_valid_data(self):
        form_data = {"username": "test_user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data.get("username"), form_data.get("username")
        )

    def test_driver_search_form_field_label(self):
        self.assertEqual(self.form.fields["username"].label, "")

    def test_driver_search_form_field_placeholder(self):
        self.assertEqual(
            self.form.fields["username"].widget.attrs["placeholder"],
            "Search by username")


class TestCarSearchForm(TestCase):
    def setUp(self) -> None:
        self.form = CarSearchForm()

    def test_car_search_form_valid_data(self):
        form_data = {"model": "test_model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data.get("model"), form_data.get("model")
        )

    def test_car_search_form_field_label(self):
        self.assertEqual(self.form.fields["model"].label, "")

    def test_car_search_form_field_placeholder(self):
        self.assertEqual(
            self.form.fields["model"].widget.attrs["placeholder"],
            "Search by model")


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.form = ManufacturerSearchForm()

    def test_manufacturer_search_form_valid_data(self):
        form_data = {"name": "test_name"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data.get("name"), form_data.get("name")
        )

    def test_manufacturer_search_form_field_label(self):
        self.assertEqual(self.form.fields["name"].label, "")

    def test_manufacturer_search_form_field_placeholder(self):
        self.assertEqual(
            self.form.fields["name"].widget.attrs["placeholder"],
            "Search by name")
