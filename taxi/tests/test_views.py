from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(200, response.status_code)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="bob123",
            password="test123",
        )
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")
        self.manufacturers = Manufacturer.objects.all()
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(self.manufacturers)
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(200, response.status_code)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.drivers = [
            get_user_model().objects.create_user(
                username=f"bob123{i}",
                password="test123",
                first_name="Bob",
                last_name="James",
                license_number=f"ABC1234{i}",
            )
            for i in range(3)
        ]
        self.client.force_login(self.drivers[0])

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(self.drivers)
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(200, response.status_code)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="bob123",
            password="test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.cars = Car.objects.bulk_create([
            Car(
                model=f"A{i}",
                manufacturer=self.manufacturer,
            )
            for i in range(5)
        ])
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(self.cars)
        )
