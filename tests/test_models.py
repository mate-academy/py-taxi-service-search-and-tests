from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_1",
            country="Test republic",
        )

        self.driver = get_user_model().objects.create_user(
            username="Test username",
            first_name="Name first",
            last_name="Name last",
            password="Test_12345",
            license_number="ABC12345",
        )

        self.car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name}"
            f" {self.driver.last_name})",
        )

    def test_driver_get_absolute_url(self) -> None:
        url = self.driver.get_absolute_url()

        test_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk},
        )
        self.assertEqual(url, test_url)

    def test_driver_license_number(self) -> None:
        self.assertEqual(self.driver.username, "Test username")
        self.assertTrue(self.driver.check_password("Test_12345"))
        self.assertEqual(self.driver.license_number, "ABC12345")
