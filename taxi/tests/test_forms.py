from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)
from taxi.models import Manufacturer, Car

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="ATM55555",
        )
        self.client.force_login(self.user)

    def test_driver_username_search_form(self):
        form_data = {"username": self.user.username}

        form = DriverUsernameSearchForm(data=form_data)
        response = self.client.get(DRIVER_LIST_URL, data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="ATM55555",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Test"
        )
        self.car = Car.objects.create(
            model="Sedan",
            manufacturer=self.manufacturer
        )

    def test_car_model_search_form(self):
        form_data = {"model": self.car.model}

        form = CarModelSearchForm(data=form_data)
        response = self.client.get(CAR_LIST_URL, data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_car_model_search_no_results(self):
        search_url = reverse("taxi:car-list")
        form_data = {"model": "Tesla"}
        response = self.client.get(search_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.car.model)


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="ATM55555",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Test"
        )

    def test_manufacturer_name_search_form(self):
        form_data = {"name": self.manufacturer.name}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_model_search_no_results(self):
        search_url = reverse("taxi:manufacturer-list")
        form_data = {"name": "Audi"}
        response = self.client.get(search_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.manufacturer.name)
