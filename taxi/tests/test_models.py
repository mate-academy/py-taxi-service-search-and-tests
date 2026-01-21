from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import (
    Manufacturer,
    Car
)


class ModelTests(TestCase):
    def setUp(self):
        self.test_driver = get_user_model().objects.create_user(
            username="UserName",
            first_name="FirstName",
            last_name="LastName",
            email="Email@Address",
            license_number="ADM12345",
            password="<PASSWORD>",
        )
        self.test_manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )

        self.test_car = Car.objects.create(
            model="Model",
            manufacturer=self.test_manufacturer)
        self.test_car.drivers.add(self.test_driver,)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.test_manufacturer),
            f"{self.test_manufacturer.name} {self.test_manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.test_driver),
                         f"{self.test_driver.username} ({self.test_driver.first_name} {self.test_driver.last_name})")

    def test_car_str(self):
        self.assertEqual(str(self.test_car), self.test_car.model)

    def test_set_valid_license_number(self):
        self.test_driver.license_number = "ADM12346"
        self.assertEqual(self.test_driver.license_number, "ADM12346")

    def test_set_invalid_license_number(self):
        with self.assertRaises(ValidationError):
            self.test_driver.license_number = "AD1234"
            self.test_driver.full_clean()

    def test_password_is_correct(self):
        self.assertTrue(self.test_driver.check_password("<PASSWORD>"))

    def test_correct_label(self):
        license_number_label = self.test_driver._meta.get_field("license_number").verbose_name
        self.assertEqual(license_number_label, "license number")

    def test_car_model_max_length(self):
        field_max_length = self.test_car._meta.get_field("model").max_length
        self.assertEqual(field_max_length, 255)

    def test_driver_absolute_url(self):
        test_driver_absolute_url = self.test_driver.get_absolute_url()
        self.assertEqual(
            test_driver_absolute_url,
            f"/drivers/{self.test_driver.id}/"
        )
