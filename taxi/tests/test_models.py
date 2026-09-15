from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car),
            "X5"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="john",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="john",
            password="testpass123",
            license_number="ABC12345"
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
