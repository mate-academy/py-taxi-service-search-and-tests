from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


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

    def test_object_name_is_name_country(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), "Fiat Italy")


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
            first_name="Bob",
            last_name="Smith",
            license_number="AB123",
        )

    def test_username_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("username").verbose_name

        self.assertEqual(field_label, "username")

    def test_password_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("password").verbose_name

        self.assertEqual(field_label, "password")

    def test_license_number_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name

        self.assertEqual(field_label, "license number")

    def test_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        license_number = driver.license_number

        self.assertEqual(license_number, "AB123")
        self.assertTrue(driver.check_password("test1234"))

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        url = driver.get_absolute_url()

        self.assertEqual(url, "/drivers/1/")

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(str(driver), "test_user (Bob Smith)")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        driver = get_user_model().objects.create_user(
            username="test_user"
        )

        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        car.drivers.add(driver)
        car.save()

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), "X5")
