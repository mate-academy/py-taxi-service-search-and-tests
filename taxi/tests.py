from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer, Driver

User = get_user_model()


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
            license_number="123456"
        )
        self.client = Client()
        self.client.login(username="testuser", password="12345")

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Q7",
            manufacturer=self.manufacturer2
        )

        self.driver1 = User.objects.create_user(
            username="john",
            license_number="654321"
        )
        self.driver2 = User.objects.create_user(
            username="mary",
            license_number="987654"
        )

    def test_car_search(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertIn(self.car2, cars)

        response = self.client.get(url, {"model": "X5"})
        cars = response.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})
        drivers = response.context["driver_list"]
        self.assertIn(self.driver1, drivers)
        self.assertNotIn(self.driver2, drivers)

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BMW"})
        manufacturers = response.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)
