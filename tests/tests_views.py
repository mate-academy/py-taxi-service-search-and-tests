from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicAccessTests(TestCase):
    def test_manufacturer_public(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_public(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_public(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="vasya.pupkin",
            first_name="Vasya",
            last_name="Pupkin",
            password="345ert345",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="X5", manufacturer=self.manufacturer
        )
        self.car = Car.objects.create(
            model="RAV4", manufacturer=self.manufacturer2
        )

    def test_manufacturers_privat(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturers,
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_cars_privat(self):
        response = self.client.get(CAR_URL)
        cars = list(Car.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_drivers_privat(self):
        drivers = list(get_user_model().objects.all())
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            drivers,
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
