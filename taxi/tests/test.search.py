from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_driver",
            password="test12345"
        )

        self.client.force_login(self.driver)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car1 = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer2
        )

        self.driver2 = Driver.objects.create_user(
            username="another_driver",
            password="test12345"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )

        self.assertContains(response, "test_driver")
        self.assertNotContains(response, "another_driver")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "M5"}
        )

        self.assertContains(response, "M5")
        self.assertNotContains(response, "Corolla")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")
