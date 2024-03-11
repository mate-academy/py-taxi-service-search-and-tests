from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverSearchForm,
                        ManufacturerSearchForm,
                        CarSearchForm)


class FormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "test123pswrd",
            "password2": "test123pswrd",
            "first_name": "John",
            "last_name": "Cena",
            "license_number": "TST12345",
        }

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "test_username"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_username")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_name")

    def test_cars_search_form(self):
        form = CarSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")
