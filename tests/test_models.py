from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse

from taxi.models import Manufacturer, Car


class ModelsTestsSetUp(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="test"
        )
        self.driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="Test First",
            last_name="test_last",
            license_number="AEC11111"
        )

        self.driver2 = self.driver = get_user_model().objects.create(
            username="test1",
            password="test123",
            first_name="Test First",
            last_name="test_last",
            license_number="ZDC11111"
        )
        self.car_model = "test"
        self.car = Car.objects.create(
            model=self.car_model,
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(str(self.manufacturer),
                        f"{self.manufacturer.name} {self.manufacturer.country}")

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)


class TestDriverModel(ModelsTestsSetUp):
    def test_create_driver_with_license_number(self) -> None:
        username = "testovych"
        password = "test123"
        license_number = "ADC11111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_get_absolute_url(self) -> None:
        url = self.driver.get_absolute_url()
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )

        self.assertEqual(url, expected_url)


class TestCar(ModelsTestsSetUp):
    def test_car_creation(self) -> None:
        self.car.drivers.add(self.driver, self.driver2)
        self.assertEqual(self.car.model, self.car_model)
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())

