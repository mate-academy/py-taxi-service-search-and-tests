from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="first",
            last_name="last"
        )

        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEquals(str(car), car.model)

    def test_create_driver_licence(self) -> None:
        username = "test"
        password = "test1234"
        license_number = "tes12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
