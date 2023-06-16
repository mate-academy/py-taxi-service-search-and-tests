from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="tests",
            country="country")
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        driver = get_user_model().objects.create_user(
            username="tests",
            password="test1234",
            first_name="Test first",
            last_name="Test last",
            license_number="TES12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="tests",
            country="country"
        )
        car = Car.objects.create(
            model="tests",
            manufacturer=manufacturer,

        )
        car.drivers.add(driver)
        car.save()
        self.assertEquals(str(car), car.model)

    def test_driver_str(self):
        username = "tests"
        password = "test1234"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Test first",
            last_name="Test last",
            license_number=license_number,
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)


class DriverTest(TestCase):
    def setUp(self):
        username = "tests"
        password = "test1234"
        license_number = "TES12345"
        get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Test first",
            last_name="Test last",
            license_number=license_number,
        )

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_date_of_verbose_name(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")
