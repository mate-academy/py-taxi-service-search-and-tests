from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewsTest(TestCase):
    def test_manufacturer_login_required(self):
        self.assertNotEqual(
            self.client.get(
                MANUFACTURER_LIST_URL
            ).status_code, 200
        )

    def test_car_login_required(self):
        self.assertNotEqual(self.client.get(CAR_LIST_URL).status_code, 200)

    def test_driver_login_required(self):
        self.assertNotEqual(self.client.get(DRIVER_LIST_URL).status_code, 200)


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123", license_number="ABC12345"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="BMW", country="Germ")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="X5", manufacturer=manufacturer)
        get_user_model().objects.create_user(
            username="john", password="test123", license_number="XYZ99999"
        )

    def test_manufacturer_search(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "bmw"})
        self.assertContains(res, "BMW")
        self.assertNotContains(res, "Toyota")

    def test_car_search(self):
        res = self.client.get(CAR_LIST_URL, {"model": "camry"})
        self.assertContains(res, "Camry")
        self.assertNotContains(res, "X5")

    def test_driver_search(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        self.assertContains(res, "john")
        self.assertNotContains(res, "jane_smith")
