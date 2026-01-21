from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "john",
            "license_number": "LCA12345",
            "first_name": "John",
            "password1": "test1234!",
            "password2": "test1234!",
            "last_name": "Smith",
            "email": "test@gmail.com",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )
        self.assertEqual(form.cleaned_data["first_name"],
                         form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"],
                         form_data["last_name"])

    def test_manufacturer_name_search_form_is_valid(self):
        form_data = {"name": "test"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_driver_username_search_form_is_valid(self):
        form_data = {"username": "test_username"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    def test_car_model_search_form_is_valid(self):
        form_data = {"model": "test_model"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
