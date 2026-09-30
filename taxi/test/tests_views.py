from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class SearchTests(TestCase):
    def setUp(self):
        self.manufacturer_one = Manufacturer.objects.create(
            name="Test 1",
            country="Test Country"
        )
        self.manufacturer_two = Manufacturer.objects.create(
            name="Test 2",
            country="Test Country"
        )

        self.car_one = Car.objects.create(
            model="Test 1",
            manufacturer=self.manufacturer_one
        )
        self.car_two = Car.objects.create(
            model="Test 2",
            manufacturer=self.manufacturer_two
        )

        self.user_one = get_user_model().objects.create_user(
            username="test_1",
            password="test123",
            license_number="ABC12345"
        )
        self.user_two = get_user_model().objects.create_user(
            username="test_2",
            password="test456",
            license_number="ABD12845"
        )
        self.client.force_login(self.user_one)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": self.manufacturer_one.name}
        )
        self.assertIn(
            self.manufacturer_one,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer_two,
            response.context["manufacturer_list"]
        )

    def test_search_car_by_model(self):
        response = self.client.get(CAR_URL, {"model": self.car_one.model})
        self.assertIn(self.car_one, response.context["car_list"])
        self.assertNotIn(self.car_two, response.context["car_list"])

    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "_1"})
        self.assertIn(self.user_one, response.context["driver_list"])
        self.assertNotIn(self.user_two, response.context["driver_list"])
