from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345",
        )

        self.client.login(
            username="testuser",
            password="test12345",
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2,
        )

        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="DEF67890",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="alice",
            password="test12345",
            license_number="GHI12345",
        )

    def test_search_driver(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "alice")

    def test_search_car(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Cor"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "X5")

    def test_search_manufacturer(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
