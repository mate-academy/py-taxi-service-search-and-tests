from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",
            username="Test Username",
            license_number="Test License Number",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",
            username="Test Username",
            license_number="Test License Number",
        )
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.id})
        self.assertEqual(driver.get_absolute_url(), url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
