from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Driver, Manufacturer, Car


class PublicTests(TestCase):
    def test_login_required_for_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)


class LicenseValidationTests(TestCase):
    def test_license_number_validation(self):
        with self.assertRaises(Exception):
            validate_license_number("12345678")


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="test12345",
            license_number="ABC12345",
        )

        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="DEF12345",
        )

        Driver.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="GHI12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "alex_driver")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"},
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

        Car.objects.create(
            model="M3",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"},
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "M3")
