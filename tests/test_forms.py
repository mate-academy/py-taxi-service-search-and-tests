from django.test import TestCase

from taxi.forms import (
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm,
)


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "Name",
            "password1": "Test1234!@#",
            "password2": "Test1234!@#",
            "license_number": "ASD12345",
            "first_name": "Test",
            "last_name": "Testovich"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"],
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"],
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"],
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"],
        )


class SearchFormTests(TestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "john"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Toyota"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_search_forms_allow_empty_value(self):
        self.assertTrue(
            DriverSearchForm(data={"username": ""}).is_valid()
        )
        self.assertTrue(
            CarSearchForm(data={"model": ""}).is_valid()
        )
        self.assertTrue(
            ManufacturerSearchForm(data={"name": ""}).is_valid()
        )
