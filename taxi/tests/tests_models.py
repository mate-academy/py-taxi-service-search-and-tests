from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="test",
            last_name="driver",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Mitsubishi")
        car = Car.objects.create(model="Lancer X", manufacturer=manufacturer)
        self.assertEqual(str(car.model), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mitsubishi",
            country="Japane"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self) -> None:
        username = "test_driver"
        password = "driver1987"
        license_number = "QWE12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertTrue(driver)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1987",
            license_number="QWE12345",
        )

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.user.pk}
        )
        actual_url = self.user.get_absolute_url()
        self.assertEqual(expected_url, actual_url)
