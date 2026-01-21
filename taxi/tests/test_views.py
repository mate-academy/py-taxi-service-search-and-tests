from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345ghgy"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_car_searching(self):
        response = self.client.get(CAR_URL, {"model": "test1"})
        self.assertEquals(
            response.context["car_list"][0],
            Car.objects.get(model="test1")
        )


class PrivateDriverTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser1",
            password="12345ghgy",
            license_number="AMD12345"
        )
        get_user_model().objects.create_user(
            username="testuser2",
            password="12345ghfg",
            license_number="AMD12445"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_car_searching(self):
        response = self.client.get(DRIVER_URL, {"username": "testuser1"})
        self.assertEquals(
            response.context["driver_list"][0],
            Driver.objects.get(username="testuser1")
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345ghgy"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Renault", country="France")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_searching(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(MANUFACTURER_URL, {"name": "Ford"})
        self.assertEquals(
            response.context["manufacturer_list"][0],
            Manufacturer.objects.get(name="Ford")
        )
