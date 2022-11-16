from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturersTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.assertEqual(str(manufacturer), "Test name Test country")

    def test_create_manufacturer_with_name_and_country(self):
        name = "Test name"
        country = "Test country"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country,
        )
        self.assertEqual(manufacturer.name, name)
        self.assertEqual(manufacturer.country, country)


class CarsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "Test model")

    def test_create_car_with_model_and_manufacturer(self):
        model = "Test model"
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEqual(car.model, model)
        self.assertEqual(car.manufacturer, manufacturer)


class DriversTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="Test",
            password="Test123",
            first_name="Test first",
            last_name="Test last",
            license_number="Test number"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.username, "Test")
        self.assertTrue(driver.check_password("Test123"))
        self.assertEqual(driver.license_number, "Test number")

    def test_get_absolut_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
