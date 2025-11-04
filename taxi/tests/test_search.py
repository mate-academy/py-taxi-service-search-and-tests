from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="pass12345"
        )
        self.client.login(username="testuser", password="pass12345")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford", country="USA")

        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Mustang", manufacturer=self.manufacturer2)

        self.driver1 = Driver.objects.create_user(
            username="driverA", password="abc12345", license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driverB", password="abc12345", license_number="DEF12345"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"q": "toy"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "cor"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "driverA"})
        self.assertContains(response, "driverA")
        self.assertNotContains(response, "driverB")
