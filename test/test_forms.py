from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    DriverCreationForm,
    CarForm,
    CarModelSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create(
            username="admin",
            password="kljjfJJGJ123",
            email="mjbfjbf@bcb.com",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.force_login(self.admin)

    def test_driver_create(self):
        form_data = {
            "username": "driver",
            "password1": "JHGHkhjghg515",
            "password2": "JHGHkhjghg515",
            "email": "email@example.com",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "JUL12345",
        }
        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search(self):
        form_data = {
            "username": "driver_search",
        }
        form = DriverUsernameSearchForm(form_data)
        self.assertTrue(form.is_valid())

    def test_car_create(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="US")
        form_data = {
            "model": "test",
            "manufacturer": manufacturer.id,
            "drivers": [self.admin.id]
        }
        form = CarForm(form_data)
        self.assertTrue(form.is_valid())

    def test_car_search(self):
        form_data = {
            "model": "test",
        }
        form = CarModelSearchForm(form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search(self):
        form_data = {
            "name": "Test",
        }
        form = ManufacturerSearchForm(form_data)
        self.assertTrue(form.is_valid())
