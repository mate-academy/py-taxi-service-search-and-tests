from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Audi Motors", country="German")

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.get(id=1)

    def test_name_label(self):
        field_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        field_label = self.manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_manufacturer_str(self):
        expected_object_name = (
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
        self.assertEqual(str(self.manufacturer), expected_object_name)


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Audi Motors",
            country="German"
        )
        user = get_user_model().objects.create_user(
            username="Carl",
            password="qwerty"
        )
        car = Car.objects.create(model="BMW", manufacturer=manufacturer)
        car.drivers.set([user])

    def setUp(self) -> None:
        self.car = Car.objects.get(id=1)

    def test_model_label(self):
        field_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_manufacturer_label(self):
        field_label = self.car._meta.get_field("manufacturer").verbose_name
        self.assertEqual(field_label, "manufacturer")

    def test_driver_label(self):
        field_label = self.car._meta.get_field("drivers").verbose_name
        self.assertEqual(field_label, "drivers")

    def test_car_str(self):
        expected_object_name = f"{self.car.model}"
        self.assertEqual(str(self.car), expected_object_name)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="user",
            password="qwerty",
            first_name="test first",
            last_name="test last",
        )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.get(id=1)

    def test_license_number_label(self):
        field_label = (
            self.driver._meta.get_field("license_number").verbose_name
        )
        self.assertEqual(field_label, "license number")

    def test_create_driver_with_license_number(self):
        username = "user2"
        password = "qwerty"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_str(self):
        expected_object_name = (
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
