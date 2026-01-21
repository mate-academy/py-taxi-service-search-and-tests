from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            first_name="Driver",
            last_name="One",
            license_number="AB1234567"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            first_name="Driver",
            last_name="Two",
            license_number="AB1234568"
        )
        expected_url = f"/drivers/{driver.pk}/"
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_driver_license_number_unique(self):
        get_user_model().objects.create_user(
            username="driver3",
            password="password123",
            first_name="Driver",
            last_name="Three",
            license_number="AB1234569"
        )
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(
                username="driver4",
                password="password123",
                first_name="Driver",
                last_name="Four",
                license_number="AB1234569"
            )

    def test_car_has_multiple_drivers(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        driver1 = get_user_model().objects.create_user(
            username="driver5",
            password="password123",
            first_name="Driver",
            last_name="Five",
            license_number="AB1234570"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver6",
            password="password123",
            first_name="Driver",
            last_name="Six",
            license_number="AB1234571"
        )
        car.drivers.add(driver1, driver2)
        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(driver1, car.drivers.all())
        self.assertIn(driver2, car.drivers.all())
