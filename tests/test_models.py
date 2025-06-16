from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_user",
            password="PASSWORD"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Car",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            )
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test_user"
        password = "PASSWORD"
        license_number = "123456789"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_create_manufacturer_with_country(self):
        name = "Test Manufacturer"
        country = "Test Country"
        manufacturer = Manufacturer.objects.create(name=name, country=country)
        self.assertEqual(manufacturer.name, name)
        self.assertEqual(manufacturer.country, country)

    def test_create_car_with_manufacturer(self):
        model = "Test Car"
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(model=model, manufacturer=manufacturer)
        self.assertEqual(car.model, model)
        self.assertEqual(car.manufacturer, manufacturer)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="PASSWORD"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")
