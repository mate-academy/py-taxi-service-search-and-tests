from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CARS_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVERS_LIST_URL = reverse("taxi:driver-list")


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="testcountry",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        response = self.client.get(CARS_LIST_URL, {"model": "test"})
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="testcountry",
        )
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "test"})
        self.assertEqual(response.status_code, 200)

    def test_drivers_search(self):
        Driver.objects.create(
            username="test_user",
            password="testpassw0rd",
            license_number="testlicense",
        )
        response = self.client.get(DRIVERS_LIST_URL, {"model": "test"})
        self.assertEqual(response.status_code, 200)
