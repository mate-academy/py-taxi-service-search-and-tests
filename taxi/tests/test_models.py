from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Test_name", country="Test_country")

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

    def test_object_name_is_name_country(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"

        self.assertEqual(str(manufacturer), expected_object_name)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_username",
            password="test12345",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TST12345"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.username, "test_username")
        self.assertTrue(driver.check_password("test12345"))
        self.assertEqual(driver.first_name, "test_first_name")
        self.assertEqual(driver.last_name, "test_last_name")
        self.assertEqual(driver.license_number, "TST12345")

    def test_create_driver_without_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test_username2",
            password="test12345",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        try:
            driver.full_clean()
        except Exception as e:
            self.assertTrue(isinstance(e, ValidationError))

    def test_license_number_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name

        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        driver = get_user_model().objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length

        self.assertEqual(max_length, 255)

    def test_object_name_is_username_first_name_last_name(self):
        driver = get_user_model().objects.get(id=1)
        expected_object_name = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

        self.assertEqual(str(driver), expected_object_name)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test12345",
            license_number="TST12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        car.save()

    def test_model_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("model").verbose_name

        self.assertEqual(field_label, "model")

    def test_model_max_length(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("model").max_length

        self.assertEqual(max_length, 255)

    def test_manufacturer_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("manufacturer").verbose_name

        self.assertEqual(field_label, "manufacturer")

    def test_drivers_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("drivers").verbose_name

        self.assertEqual(field_label, "drivers")

    def test_object_name_is_model(self):
        car = Car.objects.get(id=1)
        expected_object_name = car.model

        self.assertEqual(str(car), expected_object_name)
