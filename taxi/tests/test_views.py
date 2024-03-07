from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.tests.test_config import (
    DRIVER_LIST_URL,
    CAR_LIST_URL,
    MANUFACTURER_LIST_URL
)


class PublicAccessTest(TestCase):
    def test_public_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_public_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_public_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_public_driver_detail(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="Driver1test!",
            license_number="TST12345",
        )
        driver_detail_url = reverse(
            "taxi:driver-detail",
            args=[self.driver.id]
        )
        response = self.client.get(driver_detail_url)
        self.assertNotEqual(response.status_code, 200)

    def test_public_car_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="Bugatti",
            country="Italy"
        )
        car = Car.objects.create(
            model="Veyron",
            manufacturer=manufacturer
        )
        car_detail_url = reverse("taxi:car-detail", args=[car.id])
        response = self.client.get(car_detail_url)
        self.assertNotEqual(response.status_code, 200)
