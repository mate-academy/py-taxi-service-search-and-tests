from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")


class DriverModelTests(TestCase):
    def test_str_method(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.assertEqual(str(driver), "driver1 (John Doe)")

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver2",
            password="testpass123",
            license_number="XYZ999"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)


class CarModelTests(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "X5")
