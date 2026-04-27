from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarModelSearchForm,
                        ManufacturerNameSearchForm, DriverUsernameSearchForm)


class FormsTests(TestCase):
    def test_driver_creation_with_license_number_form_valid(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "driver241",
            "password2": "driver241",
            "license_number": "BGD51353",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        for field_name, expected_value in form_data.items():
            self.assertEqual(
                form.cleaned_data[field_name],
                expected_value
            )


class CarModelSearchFormTests(TestCase):
    def test_car_model_search_form_placeholder(self):
        form = CarModelSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search car by model"
        )

    def test_car_model_search_form_not_required(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_car_model_search_form_long_input(self):
        form = CarModelSearchForm(data={"model": "a" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_car_model_search_form_clean_strip(self):
        form = CarModelSearchForm(data={"model": "  Tesla  "})
        self.assertTrue(form.is_valid())
        if hasattr(form, "clean_model"):
            self.assertEqual(form.cleaned_data["model"], "Tesla")


class ManufacturerNameSearchFormTests(TestCase):
    def test_search_form_placeholder(self):
        form = ManufacturerNameSearchForm()
        placeholder = form.fields["name"].widget.attrs["placeholder"]
        self.assertEqual(placeholder, "Search manufacturer name")

    def test_search_form_is_not_required(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_search_form_name_strip(self):
        form = ManufacturerNameSearchForm(data={"name": "  Toyota  "})
        self.assertTrue(form.is_valid())
        if "name" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["name"], "Toyota")


class DriverUsernameSearchFormTests(TestCase):
    def test_driver_username_search_form_placeholder(self):
        form = DriverUsernameSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search driver by username"
        )

    def test_driver_username_search_form_not_required(self):
        form = DriverUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_driver_username_search_form_max_length(self):
        form = DriverUsernameSearchForm(data={"username": "a" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
