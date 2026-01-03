from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )

        self.username = "Test.username"
        self.password = "testpassword"
        self.first_name = "first name test"
        self.last_name = "last name test"
        self.license_number = "ABA12345"

        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            license_number=self.license_number,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(self.driver.check_password(self.password))

    def test_driver_get_absolute_url(self):
        driver_url = self.driver.get_absolute_url()
        url_expected = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk},
        )

        self.assertEqual(url_expected, driver_url)
