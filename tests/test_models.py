from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_car_str(self):
        Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(model="test", manufacturer_id=1)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test",
            password="qwerty1",
            first_name="test first",
            last_name="test last",
            license_number="test"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_add_license_number_to_driver(self):
        username = "test"
        password = "qwerty1"
        license_number = "test license number"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")
