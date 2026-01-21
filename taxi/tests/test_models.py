from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="TEST",
            first_name="test",
            last_name="TeSt"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="jane_doe",
            first_name="Jane",
            last_name="Doe",
            license_number="87654321",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test123124234"
        license_number = "AA2342AA"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="test",
            last_name="TeSt",
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test444", country="Test1111"
        )
        car = Car.objects.create(
            model="TestBMW5_turbo_dream",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
