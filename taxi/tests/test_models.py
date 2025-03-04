from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self):
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Mazda",
            country="Test country 1",
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Ford",
            country="Test country 2",
        )

    def test_manufacturer_create(self):
        self.assertEqual(self.manufacturer_1.name, "Mazda")
        self.assertEqual(self.manufacturer_1.country, "Test country 1")
        self.assertEqual(Manufacturer.objects.count(), 2)

    def test_manufacturer_max_length_fields(self):
        self.assertEqual(
            self.manufacturer_1._meta.get_field("name").max_length, 255
        )
        self.assertEqual(
            self.manufacturer_1._meta.get_field("country").max_length, 255
        )

    def test_manufacturer_ordering(self):
        self.assertEqual(Manufacturer.objects.first(), self.manufacturer_2)

    def test_manufacturer_name_unique(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(
                name="Mazda",
                country="Test country 1",
            )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer_1),
            f"{self.manufacturer_1.name} {self.manufacturer_1.country}"
        )


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="1qazcde3",
            license_number="AAA11111"
        )

    def test_driver_create(self):
        self.assertEqual(self.driver.username, "user")
        self.assertTrue(self.driver.check_password("1qazcde3"))
        self.assertEqual(self.driver.license_number, "AAA11111")

    def test_driver_max_length_license(self):
        self.assertEqual(
            self.driver._meta.get_field("license_number").max_length, 255
        )

    def test_driver_license_number_unique(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="user_2",
                password="1qazcde3",
                license_number="AAA11111"
            )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class CarModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="1qazcde3",
            license_number="AAA11111"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Test country 1",
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_driver_create(self):
        self.assertEqual(self.car.model, "test")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, self.car.drivers.all())

    def test_car_max_length_model(self):
        self.assertEqual(
            self.car._meta.get_field("model").max_length, 255
        )

    def test_car_related_name(self):
        self.assertEqual(
            self.car._meta.get_field("drivers")._related_name, "cars"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.car),
            self.car.model
        )
