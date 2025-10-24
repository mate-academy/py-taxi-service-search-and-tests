from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.encoding import force_str

from taxi.models import Manufacturer, Car, Driver


DRIVER_URL = "/drivers/"


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="clsBMW",
            country="Germany",
        )

    def test_manufacturer_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_manufacturer_country_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_manufacturer_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_country_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(expected_object_name, str(manufacturer))

    def test_manufacturer_ordering(self):
        manufacturer = Manufacturer.objects.get(id=1)
        manufacturer1 = Manufacturer.objects.create(
            name="Test name 1", country="Test country 1"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="Test name 3", country="Test country 2"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Test name 2", country="Test country 3"
        )
        self.assertListEqual(
            list(Manufacturer.objects.all()),
            [manufacturer1, manufacturer2, manufacturer3, manufacturer],
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_user",
            password="password",
            first_name="first",
            last_name="last",
            license_number="ABC12345",
        )

    def test_driver_moder_verbose_name(self):
        self.assertEqual(
            force_str(Driver._meta.verbose_name),
            "driver"
        )

    def test_driver_moder_verbose_name_plural(self):
        self.assertEqual(
            force_str(Driver._meta.verbose_name_plural),
            "drivers"
        )

    def test_driver_license_number_exists(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            driver.license_number,
            "ABC12345",
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(),
            f"{DRIVER_URL}{driver.pk}/"
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.driver = Driver.objects.create(
            username="test_user",
            password="password",
            first_name="first",
            last_name="last",
            license_number="ABC12345",
        )
        self.car.drivers.add(self.driver)

    def test_car_model_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_car_has_manufacturer(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_car_remove_manufacture(self):
        self.manufacturer.delete()
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

    def test_car_reverse_related_name_cars(self):
        self.assertIn(self.car, self.driver.cars.all())
