from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.name = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.name)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Test",
            country="Test land"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.name = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.name)

    def test_retrieve_car(self):
        Car(model="Test")
        Car(model="Test2")

        response = self.client.get(CAR_URL)
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.name = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.name)

    def test_retrieve_driver(self):
        Driver.objects.create(username="Test123", license_number="ABC12345")

        response = self.client.get(DRIVER_URL)
        driver = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
