from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTestsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="Test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(first_name="Driver",
                                            last_name="Test")

    def test_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(actual_url, expected_url)

    def test_driver_str(self):
        driver = Driver.objects.create(
            license_number="QWE738294",
            username="test_name",
            password="test123456",
            first_name="test_first",
            last_name="test_last",)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "QWE837265"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class CarTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(car.model, str(car))
