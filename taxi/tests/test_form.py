from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)


class DriverCreateFormTests(TestCase):
    def test_driver_create_with_licence_lastname_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "model"
        form_data = {field: "test_model"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class ManufacturerSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_model"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class DriverSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "username"
        form_data = {field: "test_model"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
