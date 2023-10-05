from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Kia", country="South Korea"
        )
        self.driver = Driver.objects.create_user(
            license_number="AMD56849",
            username="test",
            password="12345"
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="Sorento", manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self) -> None:
        self.assertEqual(self.driver.username, "test")
        self.assertTrue(self.driver.check_password("12345"))
