from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ManufacturerCarModelTests(TestCase):
    def test_manufacturer_str(self):
        obj_manufacturer = Manufacturer.objects.create(
            name="Automobile",
            country="Country"
        )

        self.assertEquals(str(obj_manufacturer), "Automobile Country")

    def test_car_str(self):
        obj_manufacturer = Manufacturer.objects.create(
            name="Automobile",
            country="Country"
        )
        obj_car = Car.objects.create(
            model="Car",
            manufacturer=obj_manufacturer
        )

        self.assertEquals(str(obj_car), "Car")


class DriverModelTests(TestCase):
    def setUp(self) -> None:
        self.obj_driver = get_user_model().objects.create_user(
            username="user321",
            first_name="user_first",
            last_name="user_last",
            password="user12345",
            license_number="ABC12345"
        )

    def test_driver_str(self):
        obj_driver = get_user_model().objects.get(id=1)

        self.assertEquals(
            str(obj_driver), "user321 (user_first user_last)"
        )

    def test_driver_license_number(self):
        obj_driver = get_user_model().objects.get(id=1)

        self.assertTrue(obj_driver.check_password("user12345"))
        self.assertEquals(
            obj_driver.license_number, "ABC12345"
        )

    def test_driver_get_absolute_url(self):
        obj_driver = get_user_model().objects.get(id=1)

        self.assertEquals(
            obj_driver.get_absolute_url(), "/drivers/1/"
        )
