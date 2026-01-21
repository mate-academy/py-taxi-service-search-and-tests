from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self) -> None:
        obj = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(str(obj), f"{obj.name} {obj.country}")

    def test_driver_str(self) -> None:
        obj = Driver.objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.assertEqual(
            str(obj),
            f"{obj.username} ({obj.first_name} {obj.last_name})"
        )

    def test_car_str(self) -> None:
        obj_manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        obj = Car.objects.create(
            model="test_model",
            manufacturer=obj_manufacturer
        )
        self.assertEqual(str(obj), obj.model)

    def test_create_author_with_password(self) -> None:
        username = "123"
        password = "password123"
        license_number = "TES12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
