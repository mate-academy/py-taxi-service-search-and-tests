from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Fiat", country="Italy")

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="TRY12345"
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), expected_object_name)

    def test_license_number_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        driver = Driver.objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), '/drivers/1/')


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Fiat", country="Italy")
        Car.objects.create(
            model="Fiat Tipo",
            manufacturer=manufacturer
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_object_name = car.model
        self.assertEqual(str(car), expected_object_name)
