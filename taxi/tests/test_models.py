from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        obj_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), obj_str)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(license_number="QWE123")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_str(self):
        driver = Driver.objects.get(id=1)
        obj_str = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), obj_str)

    def test_verbose_name_plural(self):
        driver = Driver.objects.get(id=1)
        verbose_name_plural = driver._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, "drivers")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "test license number 123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Driver.objects.create(license_number="QWE123")
        Car.objects.create(model="Audi", manufacturer=manufacturer)

    def test_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
