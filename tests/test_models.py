from django.contrib.auth import get_user_model

from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="test1",
            country="test"
        )
        self.assertEqual(str(manufacturer_),
                         f"{manufacturer_.name} {manufacturer_.country}"
                         )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="12345678",
            first_name="test12",
            last_name="test34",
        )

        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})"
                         )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "Victoria"
        password = "0987654321"
        license_number = "CC6537AA"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
