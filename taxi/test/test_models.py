from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Subaru",
            country="Japan"
        )
        driver = Driver.objects.create(
            username="reichikku",
            first_name="Slawa",
            last_name="Melnyk",
            license_number="IKO0448"
        )
        car = Car.objects.create(
            model="Subaru Forester",
            manufacturer=Manufacturer.objects.get(name="Subaru"),
        )
        car.drivers.add(driver)

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)

    def test_driver_str_method(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = (f"{driver.username} "
                                f"({driver.first_name} "
                                f"{driver.last_name})")
        self.assertEqual(str(driver), expected_object_name)

    def test_car_str_method(self):
        car = Car.objects.get(id=1)
        expected_object_name = f"{car.model}"
        self.assertEqual(str(car), expected_object_name)

    def test_create_driver_with_license_number(self):
        username = "qzish"
        password = "test123"
        license_number = "IOA2211"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
