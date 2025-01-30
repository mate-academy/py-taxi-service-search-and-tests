from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from taxi.forms import (
    ManufacturerSearchNameForm,
    CarSearchModelForm,
    DriverSearchNameForm,
)
from taxi.models import Manufacturer, Car, Driver


class SearchTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.client = Client()

        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            license_number="OLD12322",
        )
        self.client.force_login(self.driver)
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_search(self):
        form_data = {
            "name": "TestName",
        }
        form = ManufacturerSearchNameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search(self):
        form_data = {
            "model": "TestModel",
        }
        form = CarSearchModelForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search(self):
        form_data = {
            "username": "testuser",
        }
        form = DriverSearchNameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
