from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.assertEquals(str(car), car.model)
