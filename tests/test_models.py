from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name1", country="County1"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_creation(self):
        driver = Driver.objects.create(
            license_number="12345678"
        )
        driver_str = (f"{driver.username} "
                      f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), driver_str)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test1111"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(license_number, driver.license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        model = "Model1"
        manufacturer = Manufacturer.objects.create(
            name="Name1", country="County1"
        )
        username = "test"
        password = "test1111"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), car.model)
