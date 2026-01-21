from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Testland"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test1234"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="Test First",
            last_name="Test Last",
            password="test1234"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="test1234",
            license_number="XYZ12345"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", args=[driver.id])
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Testland"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_car_driver_relationship(self):
        manufacturer = Manufacturer.objects.create(
            name="TestCar",
            country="USA"
        )
        car = Car.objects.create(model="XModel", manufacturer=manufacturer)

        driver = get_user_model().objects.create_user(
            username="driver_test",
            password="12345test",
            license_number="LIC12345"
        )
        car.drivers.add(driver)

        self.assertIn(driver, car.drivers.all())
        self.assertIn(car, driver.cars.all())
