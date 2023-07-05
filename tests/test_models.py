from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
            first_name="Test First",
            last_name="Test Last",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )

        self.assertEquals(
            str(car),
            car.model
        )

    def test_driver_str(self):
        self.assertEquals(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test_user_create"
        password = "1qazcde3"
        license_number = "CRE54321"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        self.assertEquals(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )
