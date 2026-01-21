from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        self.driver1 = Driver.objects.create(
            username="driver1", license_number="ABC123"
        )
        self.driver2 = Driver.objects.create(
            username="driver2", license_number="DEF456"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer1", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer2", country="Germany"
        )

        self.car1 = Car.objects.create(
            model="CarModel1", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="CarModel2", manufacturer=self.manufacturer2
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"driver_search_query": "driver1"}
        )
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"car_search_query": "CarModel1"}
        )
        self.assertContains(response, "CarModel1")
        self.assertNotContains(response, "CarModel2")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"manufacturer_search_query": "Manufacturer1"}
        )
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")
