from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufact_ = Manufacturer.objects.create(
            name="test",
            country="test country"
        )

        self.assertEqual(
            str(manufact_),
            f"{manufact_.name} {manufact_.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            password="testFry27uw",
            first_name="Test-name First",
            last_name="Test-name Last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufact_ = Manufacturer.objects.create(name="testing")
        car = Car.objects.create(
            model="TestoModelo",
            manufacturer=manufact_,
        )

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_a_license(self):
        username = "test username"
        password = "testFry27uw"
        first_name = "Test-name First"
        last_name = "Test-name Last"
        license_number = "TES56765"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
