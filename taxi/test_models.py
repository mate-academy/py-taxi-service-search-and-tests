from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTests(TestCase):
    def test_manufacturer_name_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        self.assertEqual(
            str(manufacturer).strip(),
            manufacturer.name.strip()
        )

    def test_manufacturer_country_str(self):
        manufacturer = Manufacturer.objects.create(country="Germany")
        self.assertEqual(
            str(manufacturer).strip(),
            manufacturer.country.strip()
        )


class DriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="user1", license_number="12345678"
        )

    def test_license_number_uniqueness(self):
        get_user_model().objects.create(
            username="user4", license_number="AO8888AO"
        )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(
                username="user5", license_number="AO8888AO"
            )

    def test_model_meta_verbose_name(self):
        self.assertEqual(self.driver._meta.verbose_name, "driver")

    def test_model_meta_verbose_name_plural(self):
        self.assertEqual(self.driver._meta.verbose_name_plural, "drivers")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="Test First",
            last_name="Test Last",
            license_number="98765432",
        )
        expected_str = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(str(driver), expected_str)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="jane_doe",
            first_name="Jane",
            last_name="Doe",
            license_number="87654321",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )


class CarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW")

    def test_car_str(self):
        car = Car.objects.create(
            model="i4 Competition",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car).strip(), car.model.strip())

    def test_create_car(self):
        driver1 = Driver.objects.create(
            username="Driver1",
            license_number="AO8888AO"
        )
        driver2 = Driver.objects.create(
            username="Driver2",
            license_number="AO9999AO"
        )

        car = Car.objects.create(
            model="i4 Competition",
            manufacturer=self.manufacturer
        )

        car.drivers.add(driver1, driver2)

        self.assertEqual(car.manufacturer, self.manufacturer)

        self.assertTrue(car.drivers.filter(username="Driver1").exists())
        self.assertTrue(car.drivers.filter(username="Driver2").exists())

    def test_relations(self):
        car = Car.objects.create(
            model="i4 Competition",
            manufacturer=self.manufacturer
        )
        driver = Driver.objects.create(
            username="driver1",
            license_number="AO7777AO"
        )
        car.drivers.add(driver)

        self.assertIn(driver, car.drivers.all())
        car.drivers.remove(driver)
        self.assertNotIn(driver, car.drivers.all())
