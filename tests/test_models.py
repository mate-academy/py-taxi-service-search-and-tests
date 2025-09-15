from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_is_valid_data(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.assertEqual(manufacturer.name, "Test Manufacturer")
        self.assertEqual(manufacturer.country, "Test Country")
        self.assertEqual(Manufacturer.objects.count(), 1)

    def test_manufacturer_unique_name(self):
        Manufacturer.objects.create(name="Test Manufacturer")
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(name="Test Manufacturer")

    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="1Test Manufacturer",
                                    country="1Test Country")
        Manufacturer.objects.create(name="2Test Manufacturer",
                                    country="2Test Country")
        Manufacturer.objects.create(name="3Test Manufacturer",
                                    country="3Test Country")

        manufacturers = Manufacturer.objects.all()
        names = [manufacturer.name for manufacturer in manufacturers]
        self.assertEqual(names, ["1Test Manufacturer",
                                 "2Test Manufacturer",
                                 "3Test Manufacturer"])


class DriverModelTests(TestCase):
    def test_driver_is_valid_data(self):
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="Test Password",
            first_name="Test First",
            last_name="Test Last",
            license_number="Test License Number",
        )
        self.assertEqual(driver.username, "Test Driver")
        self.assertEqual(driver.first_name, "Test First")
        self.assertEqual(driver.last_name, "Test Last")
        self.assertEqual(driver.license_number, "Test License Number")
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_driver_unique_license_number(self):
        get_user_model().objects.create_user(
            username="Test Driver",
            password="Test Password",
            license_number="Test License Number",
        )
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="Test Driver2",
                password="Test Password2",
                license_number="Test License Number",
            )

    def test_driver_format_str(self):
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            first_name="Test First",
            last_name="Test Last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="Test Password",
            first_name="Test First",
            last_name="Test Last",
            license_number="Test License Number",
        )
        url = driver.get_absolute_url()
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(url, expected_url)


class CarModelTests(TestCase):
    def test_car_is_valid_data(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(car.model, "Test Model")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertEqual(car.manufacturer.country, "Test Country")
        self.assertEqual(Car.objects.count(), 1)

    def test_assign_multiple_drivers(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(model="Test Model", manufacturer=manufacturer)

        driver1 = get_user_model().objects.create_user(
            username="Test Driver1",
            password="pass",
            license_number="Test License Number1",
        )
        driver2 = get_user_model().objects.create_user(
            username="Test Driver2",
            password="pass",
            license_number="Test License Number2",
        )

        car.drivers.add(driver1, driver2)

        drivers = car.drivers.all()
        self.assertIn(driver1, drivers)
        self.assertIn(driver2, drivers)
        self.assertEqual(car.drivers.count(), 2)

    def test_car_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            f"{car.model}"
        )
