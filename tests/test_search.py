from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="driver_one",
            password="12345",
            license_number="AAA111",
        )
        self.driver2 = Driver.objects.create_user(
            username="driver_two",
            password="12345",
            license_number="BBB222",
        )

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford")

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "one"}
        )
        self.assertContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_car_search(self):
        response = self.client.get(reverse(
            "taxi:car-list"),
            {"model": "corolla"}
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_manufacturer_search(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "toyota"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
