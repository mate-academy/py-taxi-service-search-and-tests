from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_car(self) -> None:
        response_car = self.client.get(CAR_URL)

        self.assertNotEqual(response_car.status_code, 200)

    def test_login_required_manufacturer(self) -> None:
        response_manufacturer = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response_manufacturer.status_code, 200)

    def test_login_required_driver(self) -> None:
        response_driver = self.client.get(DRIVER_URL)

        self.assertNotEqual(response_driver.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="author123456",
            license_number="BBB12345",
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )
        Manufacturer.objects.create(
            name="TestManufacturer2",
            country="TEST2"
        )

        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )
        Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)

        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
