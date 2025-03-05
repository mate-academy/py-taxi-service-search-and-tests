from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import (
    DriverSearchForm,
    DriverCreationForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from .models import Driver, Car, Manufacturer


class SearchFeatrueTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer
        )

    def test_index_view_should_be_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_list_view_should_be_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_should_create_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Hey",
            "last_name": "Taey"
        })
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_should_valid(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Model S"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Tesla"})
        self.assertTrue(form.is_valid())
