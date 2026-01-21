from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    @classmethod
    def setUp(cls):
        Manufacturer.objects.create(
            name="Test_manufacturer",
            country="Test_country",
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="testuser",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_licence(self):
        username = "testuser"
        password = "testpassword123"
        license_number = "TES12356"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
