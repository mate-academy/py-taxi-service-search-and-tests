from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="test_brand",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Mazda", country="Japan")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car(self):
        Car.objects.create(
            model="Model_1",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="Model_2",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(CAR_URL)
        Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver(self):
        Driver.objects.create_user(
            username="first_user",
            password="first12345",
            first_name="test_name1",
            last_name="test_surname1",
            license_number="HJK94659"
        )
        Driver.objects.create_user(
            username="second_user",
            password="second09876",
            first_name="test_name2",
            last_name="test_surname2",
            license_number="LDR53956"
        )
        response = self.client.get(DRIVER_URL)
        Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
