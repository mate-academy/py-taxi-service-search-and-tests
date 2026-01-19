from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        driver = Driver.objects.create(
            username="test",
            first_name="Test first",
            last_name="Test last",
            license_number="test license number"
        )
        driver.set_password("test123")
        driver.save()

    def test_get_str(self) -> None:
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self) -> None:
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self) -> None:
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.username, "test")
        self.assertTrue(driver.check_password("test123"))
        self.assertEqual(driver.license_number, "test license number")


class CarModelTests(TestCase):
    def test_get_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)


class ManufacturerModelTests(TestCase):
    def test_get_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
