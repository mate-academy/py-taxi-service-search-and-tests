from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)

        self.driver2 = get_user_model().objects.create_user(
            username="johnny",
            password="pass456",
            license_number="XYZ67890"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"q": "driver1"}
        )
        self.assertContains(response, "driver1")

    def test_search_car_by_model(self):
        response = self.client.get(reverse(
            "taxi:car-list"),
            {"q": "Corolla"}
        )
        self.assertContains(response, "Corolla")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"q": "Toyota"}
        )
        self.assertContains(response, "Toyota")

    def test_search_driver_by_license_number(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"q": "XYZ67890"}
        )
        self.assertContains(response, "johnny")
