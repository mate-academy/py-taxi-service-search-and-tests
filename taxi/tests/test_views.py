from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="password123"
        )
        self.client.login(
            username="test_driver",
            password="password123"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_works_correctly(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toy"})

        self.assertEqual(response.status_code, 200)
        results = response.context["manufacturer_list"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Toyota")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver_car",
            password="password123"
        )
        self.client.login(
            username="test_driver_car",
            password="password123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Prius",
            manufacturer=self.manufacturer
        )

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Cam"})

        self.assertEqual(response.status_code, 200)
        results = response.context["car_list"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].model, "Camry")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver_search",
            password="password123",
            license_number="AAA11111"
        )
        self.client.login(
            username="test_driver_search",
            password="password123"
        )

    def test_driver_search_by_username(self):
        driver_matching = get_user_model().objects.create_user(
            username="johndoe",
            password="password123",
            license_number="BBB22222"
        )
        driver_non_matching = get_user_model().objects.create_user(
            username="janedoe",
            password="password123",
            license_number="CCC33333"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(driver_matching, response.context["driver_list"])
        self.assertNotIn(driver_non_matching, response.context["driver_list"])
