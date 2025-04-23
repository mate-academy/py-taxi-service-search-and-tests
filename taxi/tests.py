from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class SearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john", password="password", license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="doe", password="password", license_number="XYZ54321"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

    def test_search_driver_by_username(self):
        self.client.login(username="john", password="password")
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john")
        self.assertContains(response, "john")
        self.assertNotContains(response, "doe")

    def test_search_car_by_model(self):
        self.client.login(username="john", password="password")
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Model S")
        self.assertContains(response, "Model S")

    def test_search_manufacturer_by_name(self):
        self.client.login(username="john", password="password")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Tesla")
        self.assertContains(response, "Tesla")
