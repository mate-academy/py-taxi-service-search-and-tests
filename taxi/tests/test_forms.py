from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)


class DriverCreateFormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "license_number": "QWE12345",
            "first_name": "John",
            "last_name": "Smith",
            "password1": "user123test",
            "password2": "user123test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchFormTest(TestCase):
    def test_car_search_by_model(self):
        field = "model"
        form_data = {field: "test_model"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_by_name(self):
        field = "name"
        form_data = {field: "test_model"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class DriverSearchFormTest(TestCase):
    def test_driver_search_by_username(self):
        field = "username"
        form_data = {field: "test_model"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
