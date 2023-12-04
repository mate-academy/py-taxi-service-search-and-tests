from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverUserNameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
)


class DriverCreateFormTest(TestCase):
    def test_driver_create_with_licence_lastname_is_valid(self) -> None:
        form_data = {
            "username": "username",
            "password1": "50S1361_O$-L",
            "password2": "50S1361_O$-L",
            "first_name": "First_name",
            "last_name": "Last_name",
            "license_number": "AHN99999"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverUserNameSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "user_name"
        form_data = {field: "model_test"}
        form = DriverUserNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


#
#
class CarModelSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "model"
        form_data = {field: "model_test"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


#
class ManufacturerNameSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "manufacturer_name"
        form_data = {field: "model_test"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
