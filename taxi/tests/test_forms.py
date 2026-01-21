from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer


class DriverFormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "<PASS123WORD>",
            "password2": "<PASS123WORD>",
            "first_name": "first",
            "last_name": "last",
            "license_number": "TST12345"
        }

    def test_driver_creation_form_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_license_update_form_is_valid(self):
        form_data = {"license_number": "TST99999"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_form_not_valid_according_the_rules(self):
        for self.form_data["license_number"] in (
                "MIN123", "MAX1234567",
                "low12345", "ALPHA123",
                "NO123456", "SPC1234@"):
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "search_test_Driver"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "search_test_Driver")


class CarFormsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test-bmw", country="USX")
        self. driver1 = get_user_model().objects.create_user(
            username="driver1", password="test1234", license_number="TST12345")
        self. driver2 = get_user_model().objects.create_user(
            username="driver2", password="test1234", license_number="TST54321")

    def test_car_creation_form_is_valid(self):
        form_data = {
            "model": "test_Model",
            "manufacturer": self.manufacturer,
            "drivers": get_user_model().objects.filter(
                id__in=[self.driver1.id, self.driver2.id]
            ),
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data), list(form_data))

    def test_car_search_form(self):
        form_data = {"model": "search_test_Model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "search_test_Model")


class ManufacturerFormTest(TestCase):
    def test_manufacturer_search_form(self):
        form_data = {"name": "search_test_Manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "search_test_Manufacturer")
