from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Driver, Car


class TestSearchForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Driver.objects.create(username="Alex", license_number="12345678")
        Car.objects.create(model="Corolla", manufacturer_id=1)

    def test_manufacturer_search_form(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)

    def test_driver_search_form(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Alex"}
        )
        self.assertEqual(response.status_code, 200)

    def test_car_search_form(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Corolla"}
        )
        self.assertEqual(response.status_code, 200)

    def test_driver_creation_form(self):
        form = DriverCreationForm(
            data={
                "username": "test_username",
                "password1": "test_password",
                "password2": "test_password",
                "license_number": "VPN99999",
                "first_name": "test_first",
                "last_name": "test_last"
            }
        )
        self.assertTrue(form.is_valid())
