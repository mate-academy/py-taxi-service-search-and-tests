from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Mersedez Benz",
            country="Test Germany",
        )
        self.driver = get_user_model().objects.create_user(
            username="Rayan Gosling",
            password="Test12345",
            first_name="Test First Name",
            last_name="Test Last Name",
            license_number="BC80321",
        )

    def test_manufacturer_str(self) -> None:
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)
