from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def test_model_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(
            str(manufacturer), "BMW Germany")


class DriverTest(TestCase):
    def test_model_driver_str(self):
        driver = Driver.objects.create_user(
            username="test",
            password="12345"
        )

        self.assertEqual(
            str(driver), "test ( )")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(username="test")
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )


class CarTest(TestCase):
    def test_model_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VW",
            country="Germany"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "test")
