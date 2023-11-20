from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        name = "Name"
        country = "Country"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_car_str(self) -> None:
        model = "Model"
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )

        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), model)

    def test_driver_str(self) -> None:
        username = "username"
        password = "pswrd1234"
        first_name = "firstname"
        last_name = "lastname"

        driver = get_user_model().objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(driver),
            f"{username} ({first_name} {last_name})"
        )

    def test_driver_creation(self) -> None:
        license_number = "AAA12345"
        username = "username"
        password = "pswrd1234"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
