
from taxi.models import Manufacturer, Car
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()


class SearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TST12345"
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla", country="USA")

        self.manufacturer = self.manufacturer1
        self.car1 = Car.objects.create(
            model="Model_A", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(
            model="Model_B", manufacturer=self.manufacturer)

        self.driver1 = User.objects.create_user(
            username="john_doe",
            password="pass123",
            license_number="JHN11111"
        )
        self.driver2 = User.objects.create_user(
            username="jane_doe",
            password="pass123",
            license_number="JNE22222"
        )

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tes"}
        )

        self.assertEqual(response.status_code, 200)

        queryset = response.context["manufacturer_list"]

        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.manufacturer2)

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "model_b"}
        )

        self.assertEqual(response.status_code, 200)

        queryset = response.context["car_list"]

        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.car2)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        queryset = response.context["driver_list"]

        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.driver1)
