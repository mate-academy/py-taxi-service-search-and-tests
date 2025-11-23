from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="Test username",
            first_name="Test first name",
            last_name="Test last name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test model",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country",
            )
        )
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="Test username",
            first_name="Test first name",
            last_name="Test last name",
            password="test123",
            license_number="ASD55443",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
