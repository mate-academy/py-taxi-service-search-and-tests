from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class DriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC123",
        )

    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_retrive_driver_list(self):
        self.client.force_login(self.driver)
        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertIn(self.driver, response.context_data["driver_list"])


class CarListViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer,
        )

        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Elon",
            last_name="Musk",
            license_number="XYZ789",
        )

        self.car.drivers.add(self.driver)

    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_car_list(self):
        self.client.force_login(self.driver)
        response = self.client.get(CARS_URL)
        cars = Car.objects.select_related("manufacturer").all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertIn(self.car, response.context["car_list"])


class ManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Elon",
            last_name="Musk",
            license_number="XYZ789",
        )

    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        self.client.force_login(self.driver)
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertIn(self.manufacturer, response.context["manufacturer_list"])
