from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "test_username (Test User)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(
            model="Focus",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "Focus")

    def test_create_driver_with_license_number(self):
        license_number = "ABC98765"

        driver = get_user_model().objects.create_user(
            username="unique_user",
            password="password123",
            license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_url_driver",
            password="password123",
            license_number="URL54321"
        )

        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})

        self.assertEqual(driver.get_absolute_url(), expected_url)
