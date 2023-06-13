from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicDriverListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverDetailTest(TestCase):
    def test_login_required(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="ATM55555",
        )
        driver_detail_url = reverse(
            "taxi:driver-detail",
            args=[self.driver.id]
        )
        response = self.client.get(driver_detail_url)
        self.assertNotEqual(response.status_code, 200)


class PublicCarDetailTest(TestCase):
    def test_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer
        )
        car_detail_url = reverse("taxi:car-detail", args=[car.id])
        response = self.client.get(car_detail_url)
        self.assertNotEqual(response.status_code, 200)
