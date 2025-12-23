from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testname", country="testcountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="testfirst",
            last_name="testlast",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testname", country="testcountry"
        )
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="testfirst",
            last_name="testlast",
        )
        car = Car.objects.create(
            model="testcar",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_driver_license_number(self):
        license_number = "license_number"
        password = "<PASSWORD>"
        driver = get_user_model().objects.create_user(
            username="test",
            password=password,
            first_name="testfirst",
            last_name="testlast",
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
