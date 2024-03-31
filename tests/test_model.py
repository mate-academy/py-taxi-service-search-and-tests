from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="test_user",
            password="12345678910Qaz",
            first_name="Test",
            last_name="User"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_with_license_number(self) -> None:
        license_number = "ABC12345"

        driver = Driver.objects.create(
            username="test_user",
            password="12345678910Qaz",
            first_name="Test",
            last_name="User",
            license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)

    def test_car_name_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")

        car = Car.objects.create(model="Focus", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
