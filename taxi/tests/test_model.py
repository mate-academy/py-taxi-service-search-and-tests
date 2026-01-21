from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Bobo",
            password="Bob12345",
            first_name="Bob",
            last_name="Bobovich",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username}"
            f" ({driver.first_name}"
            f" {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        driver = get_user_model().objects.create_user(
            username="Bobo",
            password="Bob12345",
            first_name="Bob",
            last_name="Bobovich",
        )
        car = Car.objects.create(
            model="A6",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEquals(str(car), car.model)
        self.assertEquals(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "Bobo"
        password = "Bob12345"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, "ABC12345")
