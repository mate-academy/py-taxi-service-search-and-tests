from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="test_driver",
            password="test12345",
            first_name="Test",
            last_name="Driver"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_with_license_number(self) -> None:
        license_number = "ABD12345"

        driver = Driver.objects.create(
            username="test_driver",
            password="test12345",
            first_name="Test",
            last_name="Driver",
            license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)

    def test_car_name_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")

        car = Car.objects.create(model="Focus", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
