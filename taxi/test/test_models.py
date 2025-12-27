from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    def test_manufacturer_output(self):
        test_manufacture = Manufacturer.objects.create(
            name="Test manufacture",
            country="USA"
        )

        self.assertEqual(str(test_manufacture),
                         f"{test_manufacture.name} "
                         f"{test_manufacture.country}"
                         )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="new_driver",
            password="root1234",
            first_name="Name",
            last_name="Surname"
        )

    def test_driver_output(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_root_address(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    def test_car_output(self):
        test_manufacture = Manufacturer.objects.create(
            name="Test manufacture",
            country="USA"
        )

        car = Car.objects.create(
            model="M5",
            manufacturer=test_manufacture,
        )

        self.assertEqual(str(car), car.model)
