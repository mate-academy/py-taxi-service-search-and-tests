from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


DRIVER = get_user_model()


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="testname",
            country="testcountry",
        )
        cls.driver = DRIVER.objects.create_user(
            username="testusername",
            password="password",
            license_number="ABC12345",
        )
        cls.car = Car.objects.create(
            model="testmodel",
            manufacturer=cls.manufacturer,
        )
        cls.car.drivers.add(cls.driver)

    def test_manufacturer_name_field_max_length(self):
        self.assertEqual(Manufacturer._meta.get_field("name").max_length, 255)

    def test_manufacturer_country_field_max_length(self):
        self.assertEqual(
            Manufacturer
            ._meta
            .get_field("country")
            .max_length,
            255)

    def test_manufacturer_str_method(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_model_field_max_length(self):
        self.assertEqual(Car._meta.get_field("model").max_length, 255)

    def test_car_str_method(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_license_number_field_max_length(self):
        self.assertEqual(
            self.driver
            ._meta.get_field("license_number")
            .max_length,
            255)

    def test_driver_str_method(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})",
        )

    def test_driver_verbose_name(self):
        self.assertEqual(str(DRIVER._meta.verbose_name), "driver")

    def test_driver_verbose_name_plural(self):
        self.assertEqual(str(DRIVER._meta.verbose_name_plural), "drivers")
