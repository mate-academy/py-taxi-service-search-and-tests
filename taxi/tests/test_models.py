from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="america")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_format_str(self):
        driver = get_user_model().objects.create_user(
            username="testik",
            password="test1234",
            first_name="igor",
            last_name="illich")
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_car_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="america")
        car = Car.objects.create(
            model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_license(self):
        username = "testik"
        password = "test1234"
        license_number = "AMC23411"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number)
        self.assertEqual(driver.license_number, license_number)
