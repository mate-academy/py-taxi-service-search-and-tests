from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

        self.driver = Driver.objects.create_user(
            username="johnsmith",
            password="test1234",
            license_number="ABC12345"
        )

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Corolla")

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list")
            + f"?user_name={self.driver.username}")
        self.assertContains(response, self.driver.username)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"})
        self.assertContains(response, "Toyota")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"})
        self.assertContains(response, "Corolla")
