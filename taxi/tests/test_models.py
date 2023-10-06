from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):

    def setUp(self) -> None:
        self.username = "test_driver"
        self.password = "test123"
        self.license_number = "ABC12345"
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="test_first",
            last_name="test_last",
            license_number=self.license_number
        )
        self.car = Car.objects.create(
            model="testCar",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            (
                f"{self.driver.username} "
                f"({self.driver.first_name} "
                f"{self.driver.last_name})"
            )
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)

    def test_create_driver_with_license(self) -> None:
        self.assertEqual(self.driver.username, self.username)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(
            self.driver.check_password(self.password),
            self.password
        )

    def test_car_driver_relationship(self) -> None:
        self.car.drivers.add(self.driver)
        self.assertIn(self.driver, self.car.drivers.all())

    def test_get_absolute_url_return_corrected_path(self) -> None:
        url = self.driver.get_absolute_url()
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        )

        self.assertEqual(url, expected_url)

    def test_manufacturer_ordering_by_name(self) -> None:
        manufacturer3 = Manufacturer.objects.create(
            name="Z manufacturer",
            country="Country 3"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Y manufacturer",
            country="Country 2"
        )
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(manufacturers[0], self.manufacturer)
        self.assertEqual(manufacturers[1], manufacturer2)
        self.assertEqual(manufacturers[2], manufacturer3)
