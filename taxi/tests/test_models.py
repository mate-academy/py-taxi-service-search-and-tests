from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    """
    We create a superuser because we inherit the Driver from AbstractUser
    """
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = Driver.objects.create_superuser(
            username="admin",
            email="admin@mail.com",
            password="1qazcde3",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        cls.car = Car.objects.create(
            model="Jeep Compass",
            manufacturer=cls.manufacturer,
        )

    def test_admin_user_creation(self):
        self.assertEqual(self.admin_user.username, "admin")
        self.assertEqual(self.admin_user.email, "admin@mail.com")
        self.assertTrue(self.admin_user.check_password("1qazcde3"))
        self.assertTrue(self.admin_user.is_staff)

    def test_driver_str_representation(self):
        expected_name = (f"{self.admin_user.username} "
                         f"({self.admin_user.first_name} "
                         f"{self.admin_user.last_name})")
        self.assertEqual(expected_name, str(self.admin_user))

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.admin_user.get_absolute_url(),
            f"/drivers/{self.admin_user.id}/"
        )

    def test_manufacturer_str_representation(self):
        expected_name = f"{self.manufacturer.name} {self.manufacturer.country}"
        self.assertEqual(expected_name, str(self.manufacturer))

    def test_manufacturer_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(name="Jeep", country="Ukraine")

    def test_car_str_representation(self):
        expected_name = self.car.model
        self.assertEqual(expected_name, str(self.car))
