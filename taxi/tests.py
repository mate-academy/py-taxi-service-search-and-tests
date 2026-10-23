from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_search_manufacturers_by_name(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "BM"})

        self.assertIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer,
        )

        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

    def test_search_cars_by_model(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "Model"})

        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password345",
            license_number="AAA11111",
        )

        self.client.force_login(self.user)

        self.other_driver = Driver.objects.create(
            username="john_doe",
            password="password123",
            license_number="BBB22222",
        )

    def test_search_drivers_by_username(self):
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {"username": "test"})

        self.assertIn(self.user, response.context["driver_list"])
        self.assertNotIn(self.other_driver, response.context["driver_list"])
