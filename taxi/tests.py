from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")


class TaxiSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="11111"
        )
        Driver.objects.create_user(
            username="mike",
            password="67890",
            license_number="22222"
        )
        response = self.client.get(DRIVER_LIST_URL, {"username": "jo"})
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "bm"}
        )
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Mustang", manufacturer=manufacturer)
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "mod"}
        )
        self.assertContains(response, "Model S")
        self.assertNotContains(response, "Mustang")
