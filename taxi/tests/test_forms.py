from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer


class TestForms(TestCase):
    def setUp(self) -> None:
        self.driver_data = {
            "username": "test_driver",
            "license_number": "TST12345",
            "first_name": "Test",
            "last_name": "Driver",
            "password1": "PaSw1234",
            "password2": "PaSw1234",

        }

    def test_driver_creation_form(self):
        self.driver = DriverCreationForm(data=self.driver_data)
        self.assertTrue(self.driver.is_valid())
        self.assertEqual(self.driver.cleaned_data, self.driver_data)

    def test_driver_search_form(self):
        form_data = {"username": "test_driver"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_driver")

    def test_car_creation_form(self):
        driver = get_user_model().objects.create(
            username="test_driver",
            password="testPass",
            license_number="TST12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )

        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer,
            "drivers": get_user_model().objects.filter(id=driver.id)
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data), list(form_data))

    def test_car_search_form(self):
        form_data = {"model": "test_model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")

    def test_manufacturer_search_form(self):
        form_data = {"name": "test_manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_manufacturer")
