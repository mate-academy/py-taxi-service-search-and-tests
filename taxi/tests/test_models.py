from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacture = Manufacturer.objects.create(
            name="Name",
            country="Ukraine"
        )
        self.assertEquals(
            str(manufacture), f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="UserName",
            first_name="Name",
            last_name="Surname"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Ukraine"
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Model"
        )
        self.assertEqual(str(car), car.model)

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="TestUser",
            first_name="Admin",
            last_name="Last"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.id}/"
        )

    def test_license_number_validation(self):
        user = get_user_model().objects.create(
            username="TestUser",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

        self.assertEqual(user.license_number, "ABC12345")

        with self.assertRaises(ValidationError):
            user.license_number = "ABC1234"
            user.full_clean()

        with self.assertRaises(ValidationError):
            user.license_number = "ABC123456"
            user.full_clean()

        with self.assertRaises(ValidationError):
            user.license_number = "abc12345"
            user.full_clean()

        with self.assertRaises(ValidationError):
            user.license_number = "ABC12XYZ"
            user.full_clean()
