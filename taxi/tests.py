from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PublicPagesTests(TestCase):
    def test_login_required_for_driver_list(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 302)

    def test_login_required_for_car_list(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 302)

    def test_login_required_for_manufacturer_list(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 302)


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = Driver.objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA12345",
        )
        self.client.force_login(self.user)

    def test_driver_search_by_username(self) -> None:
        Driver.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="BBB12345",
        )
        Driver.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="CCC12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "alex_driver")

    def test_car_search_by_model(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="A4",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"},
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "A4")

    def test_manufacturer_search_by_name(self) -> None:
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
