from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="TES12345"
        )

        cls.manufacturer_bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        cls.manufacturer_audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer_bmw
        )
        Car.objects.create(
            model="A6",
            manufacturer=cls.manufacturer_audi
        )

        get_user_model().objects.create_user(
            username="john_driver",
            password="testpassword123",
            license_number="JOH12345"
        )
        get_user_model().objects.create_user(
            username="alice_driver",
            password="testpassword123",
            license_number="ALI12345"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "BMW"}
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "X5"}
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "A6")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"}
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "alice_driver")
