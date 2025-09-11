from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class BaseTestCase(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            license_number="ADM56987",
            username="test_username",
            password="<PASSWORD>",
            first_name="test",
            last_name="test",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test1_name", country="test1_country"
        )
        self.car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )


class DriverTest(BaseTestCase):
    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_verbose_name(self):
        self.assertEqual(self.driver._meta.verbose_name, "driver")

    def test_driver_verbose_name_plural(self):
        self.assertEqual(self.driver._meta.verbose_name_plural, "drivers")

    def test_driver_license_number_label(self):
        self.assertEqual(
            self.driver._meta.get_field("license_number").verbose_name,
            "license number"
        )

    def test_driver_license_number_max_length(self):
        self.assertEqual(self.driver._meta.get_field(
            "license_number").max_length, 255)

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(),
                         f"/drivers/{self.driver.pk}/")


class CarTest(BaseTestCase):
    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_car_model_max_length(self):
        self.assertEqual(self.car._meta.get_field("model").max_length,
                         255)

    def test_car_manufacturer_relation(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_drivers_m2m(self):
        self.car.drivers.add(self.driver)
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())


class ManufacturerTest(BaseTestCase):
    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name}"
            f" {self.manufacturer.country}",
        )

    def test_manufacturer_name_max_length(self):
        self.assertEqual(self.manufacturer._meta.get_field("name").max_length,
                         255)

    def test_manufacturer_ordering_by_name(self):
        m2 = Manufacturer.objects.create(name="test2_name",
                                         country="test2_country")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers), [self.manufacturer, m2])

    def test_manufacturer_name_unique(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(name="test1_name",
                                        country="another_country")
