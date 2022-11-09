import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL_LIST = reverse("taxi:manufacturer-list")
CAR_URL_LIST = reverse("taxi:car-list")
DRIVER_URL_LIST = reverse("taxi:driver-list")
DRIVER_URL_CREATE = reverse("taxi:driver-create")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivetManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mazda")

        response = self.client.get(MANUFACTURER_URL_LIST)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivetCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="Lincoln Continental", manufacturer_id=manufacturer.id
        )
        Car.objects.create(
            model="Toyota Yaris", manufacturer_id=manufacturer.id
        )

        response = self.client.get(CAR_URL_LIST)

        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]), list(car)
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivetDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password12355",
            license_number="TEW55044"
        )

        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first_name",
            "last_name": "Test last_name",
            "license_number": "QWE12345",
        }

        self.client.post(DRIVER_URL_CREATE, data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])
