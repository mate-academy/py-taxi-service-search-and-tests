from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        m1 = Manufacturer.objects.create(name="B", country="US")
        m2 = Manufacturer.objects.create(name="A", country="US")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers), [m2, m1])


class DriverTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="Qwert4321",
            first_name="test",
            last_name="testovych",
            license_number="AWD12345",
        )
        self.assertEqual(
            str(driver),
            (
                f"{driver.username} ({driver.first_name} {driver.last_name}) "
                f"- {driver.license_number}"
            ),
        )

    def test_driver_create_with_license_number(self):
        username = "test"
        password = "Qwert4321"
        license_number = "AWD12345"
        author = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )
        self.assertEqual(author.username, username)
        self.assertEqual(author.license_number, license_number)
        self.assertTrue(author.check_password(password))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test", password="test123", license_number="AAA111"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")


class CarTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)
