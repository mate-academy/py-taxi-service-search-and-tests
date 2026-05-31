from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Kbatrak",
            password="Bk_123haha",
            first_name="Kyrylo",
            last_name="Batrakov",
            license_number="KBB12347")

        self.manufacturer = Manufacturer.objects.create(name="Ferrari",
                                                        country="Italy")

        self.car = Car.objects.create(
            model="430", manufacturer=self.manufacturer)

        self.car.drivers.add(self.driver)

    def test_driver_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} ({self.driver.first_name} "
                         f"{self.driver.last_name})")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer),
                         f"{self.manufacturer.name} "
                         f"{self.manufacturer.country}")

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_create(self):
        username = "EddieTheBaddie"
        password = "Edd123_777"
        driver_license = "EDD12345"

        new_driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=driver_license
        )

        self.assertEqual(new_driver.username, username)
        self.assertTrue(new_driver.check_password(password))
        self.assertEqual(new_driver.license_number, driver_license)
