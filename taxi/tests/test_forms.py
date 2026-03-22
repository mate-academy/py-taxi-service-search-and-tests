from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm)


class FormsTests(TestCase):
    def test_driver_creation_form_(self):
        form_data = {
            "username": "test_user",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "license_number": "JOY12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(form.cleaned_data["license_number"], form_data["license_number"])
        user = form.save()
        self.assertTrue(user.check_password(form_data["password1"]))
        self.assertEqual(user.license_number, form_data["license_number"])


class SearchFormsTests(TestCase):
    def test_driver_empty_query_is_valid(self):
        form = DriverSearchForm({"username": ""})
        self.assertTrue(form.is_valid())
        self.assertIn("username", form.cleaned_data)

    def test_car_empty_query_is_valid(self):
        form = CarSearchForm({"model": ""})
        self.assertTrue(form.is_valid())
        self.assertIn("model", form.cleaned_data)

    def test_manufacturer_empty_query_is_valid(self):
        form = ManufacturerSearchForm({"name": ""})
        self.assertTrue(form.is_valid())
        self.assertIn("name", form.cleaned_data)
