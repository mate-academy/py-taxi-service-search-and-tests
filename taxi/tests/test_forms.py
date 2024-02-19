from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class TestForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1", password="password")

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "new_user_passw9538",
            "password2": "new_user_passw9538",
            "license_number": "VOS79458",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "CIO53950"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test Manufacturer")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test Model")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")
