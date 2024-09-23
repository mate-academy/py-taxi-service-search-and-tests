from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
            license_number="ABC12345",
            first_name="Test",
            last_name="User",
        )
        self.car = Car.objects.create(
            model="Test Car", manufacturer_id=self.manufacturer.id
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name}"
            f" {self.driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail", args=[self.driver.pk])
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
