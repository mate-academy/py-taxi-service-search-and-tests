from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def test_author_str(self) -> None:
        driver = get_user_model().objects.create(
            username="test_user",
            password="test123user",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_correct_attributes(self) -> None:
        username = "test_user"
        password = "test123user"
        first_name = "test first"
        last_name = "test last"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)

    def test_get_absolute_url(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test123user"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")


class CarModelTest(TestCase):
    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        car = Car.objects.create(model="model test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
