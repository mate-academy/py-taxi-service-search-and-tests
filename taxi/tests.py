from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.forms import (
    DriverSearchForm,
    DriverCreationForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Car, Manufacturer


class TaxiViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_index_view_requires_login(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_manufacturer_list_view_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
