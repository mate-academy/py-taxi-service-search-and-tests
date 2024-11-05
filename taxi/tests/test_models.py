from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Manufacturer, Car


class ManufacturerTests(TestCase):
    def test_manufact_str(self) -> None:
        manufact = Manufacturer.objects.create(name="Tesla", country="USA")
        self.assertEqual(str(manufact), "Tesla USA")


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create(
            username="johndoe",
            password="secret",
            first_name="John",
            last_name="Doe",
            license_number="ADF12345",
        )

    def test_license_number(self) -> None:
        self.assertEqual(self.driver.license_number, "ADF12345")

    def test_driver_str(self) -> None:
        self.assertEqual(str(self.driver), "johndoe (John Doe)")

    def test_get_absolute_url(self):
        absolute_url = self.driver.get_absolute_url()
        self.assertEqual(absolute_url, "/drivers/1/")

    def test_create_driver_without_license_shuld_raise_exception(self):
        with self.assertRaises(ValidationError):
            driver = get_user_model().objects.create(
                username="jane",
                password="secret",
                first_name="Jane",
                last_name="Doe",
            )
            driver.full_clean()


class CarTests(TestCase):
    def test_car_str(self):
        manufact = Manufacturer.objects.create(name="ZAZ", country="Ukrain")
        car = Car.objects.create(model="ZAZ-1000", manufacturer=manufact)
        self.assertEqual(str(car), "ZAZ-1000")
