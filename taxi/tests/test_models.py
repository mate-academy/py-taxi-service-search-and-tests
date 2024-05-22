from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="test_country")
        car = Car.objects.create(model="test_model",
                                 manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="glasses34",
            first_name="John",
            last_name="Sena",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "glasses34"
        password = "airdropphone"
        license_number = "CA5381IA"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_driver_absolute_url(self):
        username = "test"
        password = "testpas123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        absolute_url = driver.get_absolute_url()
        self.assertEqual(absolute_url, f"/drivers/{driver.id}/")
