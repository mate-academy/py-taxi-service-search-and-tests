from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="TestName", country="TestCountry")

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        manufacturer = Manufacturer.objects.get(id=1)
        unique = manufacturer._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_country_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def setUp(self) -> None:
        self.username = "testUser"
        self.password = "TestPassword123"
        self.license_number = "TES12345"
        get_user_model().objects.create_superuser(
            username=self.username,
            password=self.password,
            license_number=self.license_number,
        )

    def test_license_number_label(self):
        manufacturer = get_user_model().objects.get(id=1)
        field_label = (manufacturer._meta.get_field("license_number")
                       .verbose_name)
        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        manufacturer = get_user_model().objects.get(id=1)
        max_length = manufacturer._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_license_number_unique(self):
        manufacturer = get_user_model().objects.get(id=1)
        unique = manufacturer._meta.get_field("license_number").unique
        self.assertEqual(unique, True)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(str(driver.username), self.username)
        self.assertEqual(str(driver.license_number), self.license_number)
        self.assertTrue(driver.check_password(self.password))

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url_driver(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

    def test_model_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_model_max_length(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_foreign_key_between_car_and_manufacturer_label(self):
        car = Car.objects.get(id=1)
        field_label = car.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
