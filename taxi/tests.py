from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicTaxiTests(TestCase):
    def test_login_required(self):
        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateTaxiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="password123",
            license_number="AAA12345"
        )
        self.client.login(username="testdriver", password="password123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer2
        )

    def test_retrieve_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
        manufacturers = res.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertIn(self.manufacturer2, manufacturers)

    def test_search_manufacturer_by_name(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Tesla"}
        )
        manufacturers = res.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)

    def test_retrieve_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        cars = res.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertIn(self.car2, cars)

    def test_search_car_by_model(self):
        res = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Model"}
        )
        cars = res.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_retrieve_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)
        drivers = res.context["driver_list"]
        self.assertIn(self.user, drivers)

    def test_search_driver_by_username(self):
        another_driver = get_user_model().objects.create_user(
            username="another_driver",
            password="password123",
            license_number="BBB54321"
        )
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "another"}
        )
        drivers = res.context["driver_list"]
        self.assertIn(another_driver, drivers)
        self.assertNotIn(self.user, drivers)
