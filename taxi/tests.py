from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class DriverSearchTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

        self.driver2 = Driver.objects.create_user(
            username="michael",
            password="test12345",
            license_number="XYZ12345",
        )

        self.client.login(
            username="john",
            password="test12345",
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "michael")

    def test_search_with_empty_query_returns_all_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertContains(response, "michael")


class CarSearchTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

        self.client.login(
            username="john",
            password="test12345",
        )

        Car.objects.create(
            model="M3",
            manufacturer=manufacturer,
        )

        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "M3"}  # ou "model", conforme sua View
        )

        self.assertContains(response, "M3")
        self.assertNotContains(response, "Corolla")

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": ""}
        )

        self.assertContains(response, "M3")
        self.assertContains(response, "Corolla")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

        self.client.login(
            username="john",
            password="test12345",
        )

        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "BMW"}  # ou "name", conforme sua View
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_empty_search_returns_all_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": ""}
        )

        self.assertContains(response, "BMW")
        self.assertContains(response, "Toyota")
