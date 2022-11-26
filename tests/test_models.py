from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


USERNAME = "test1"
PASSWORD = "test12345"
LICENSE_NUMBER = "ABC12345"


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver = get_user_model().objects.create_user(  # type: ignore
            username=USERNAME,
            password=PASSWORD,
            first_name="Test",
            last_name="Testovetskyi",
            license_number=LICENSE_NUMBER
        )

        return super().setUp()

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str_url(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)

        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver_with_license_number(self):
        self.assertEqual(self.driver.username, USERNAME)
        self.assertTrue(self.driver.check_password(PASSWORD))
        self.assertEqual(
            self.driver.license_number,
            LICENSE_NUMBER
        )
