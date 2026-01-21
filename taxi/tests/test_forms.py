from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    DriverCreationForm,
    CarForm,
)
from taxi.models import Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        pass

    def test_car_search_form(self):
        form_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "test_name",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_create_form(self):
        form_data = {
            "username": "test_username",
            "password1": "Test_password123",
            "password2": "Test_password123",
            "license_number": "ABC12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_create_form(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="Test_password123",
            license_number="ABC12346",
        )
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [
                driver.id,
            ],
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
