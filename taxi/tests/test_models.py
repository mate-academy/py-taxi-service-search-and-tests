from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestManufacturerModel(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_name_label(self):
        field_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        field_label = self.manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        max_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        max_length = self.manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)


class TestDriverModel(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TES12345",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_license_number_validation(self):
        license_number = "TES12345"
        self.assertEqual(self.driver.license_number, license_number)

    def test_driver_username(self):
        username = "test_user"
        self.assertEqual(self.driver.username, username)

    def test_driver_check_password(self):
        password = "test_password"
        self.assertTrue(self.driver.check_password(password))

    def test_driver_first_name(self):
        first_name = "test_first_name"
        self.assertEqual(self.driver.first_name, first_name)

    def test_driver_last_name(self):
        last_name = "test_last_name"
        self.assertEqual(self.driver.last_name, last_name)

    def test_driver_license_number_label(self):
        field_label = self.driver._meta.get_field(
            "license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_driver_license_number_max_length(self):
        max_length = self.driver._meta.get_field(
            "license_number").max_length
        self.assertEqual(max_length, 255)

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class TestCarModel(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_car_model_label(self):
        field_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_car_model_max_length(self):
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_car_model_name(self):
        model = "test_model"
        self.assertEqual(self.car.model, model)
