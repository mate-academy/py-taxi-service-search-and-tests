from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


# Create your tests here.

class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_verbose_name(self):
        pass


class DriverModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        username = "test_user"
        password = "<PASSWORD>"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "test_license"
        Driver.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password("<PASSWORD>"))

    def test_driver_verbose_name(self):
        driver = Driver.objects.get(id=1)
        label = driver._meta.verbose_name
        self.assertEqual(label, "driver")

    def test_driver_plural_verbose_name(self):
        driver = Driver.objects.get(id=1)
        label = driver._meta.verbose_name_plural
        self.assertEqual(label, "drivers")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.id})
        )

    def test_driver_password(self):
        driver = Driver.objects.get(id=1)
        self.assertTrue(driver.check_password("<PASSWORD>"))
