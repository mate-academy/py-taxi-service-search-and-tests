from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="Driver_1",
            password="Password123",
        )
        self.client.login(username="Driver_1", password="Password123")

        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_search_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Tesla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")


class CarSearchViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="Driver_1",
            password="Password123",
        )
        self.client.login(username="Driver_1",
                          password="Password123")
        manufacturer = Manufacturer.objects.create(name="Honda",
                                                   country="Japan")
        Car.objects.create(model="Civic",
                           manufacturer=manufacturer)
        Car.objects.create(model="Accord",
                           manufacturer=manufacturer)

    def test_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Civic"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "Accord")


class DriverSearchViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="Driver_1",
            password="Password123",
        )
        self.client.login(username="Driver_1",
                          password="Password123")
        Driver.objects.create_user(username="Ivan",
                                   license_number="ABC12345",
                                   password="pass")
        Driver.objects.create_user(username="Petro",
                                   license_number="DEF67890",
                                   password="pass")

    def test_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "Ivan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ivan")
        self.assertNotContains(response, "Petro")
