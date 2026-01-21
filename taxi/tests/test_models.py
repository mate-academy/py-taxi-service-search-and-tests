from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase

from taxi.models import Car, Manufacturer


TEST_DATA = {
    "user1": {
        "username": "user1_username",
        "email": "user1@test.com",
        "password": "test12password",
    },
    "car1": {
        "model": "car1_model",
    },
    "manufacturer1": {
        "name": "manufacturer1_name",
        "country": "manufacturer1_country",
    },
}


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            **TEST_DATA["user1"]
        )

    def setUp(self):
        self.user = get_user_model().objects.first()

    def test_user_is_abstractuser_instance(self):
        self.assertTrue(isinstance(self.user, AbstractUser))

    def test_user_label(self):
        self.assertEqual(self.user._meta.verbose_name, "driver")

    def test_license_number_label(self):
        field_label = self.user._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_unique(self):
        self.assertTrue(self.user._meta.get_field("license_number").unique)

    def test_object_name_is_username_and_full_name_in_brackets(self):
        expected_object_name = (
            f"{self.user.username} "
            f"({self.user.first_name} {self.user.last_name})"
        )
        self.assertEqual(str(self.user), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            **TEST_DATA["manufacturer1"]
        )
        Car.objects.create(
            **TEST_DATA["car1"],
            manufacturer=manufacturer
        )

    def setUp(self):
        self.car = Car.objects.first()

    def test_car_manufacturer_required(self):
        is_null = self.car._meta.get_field("manufacturer").null
        self.assertFalse(is_null)

    def test_object_name_is_model(self):
        expected_object_name = self.car.model
        self.assertEqual(str(self.car), expected_object_name)


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(**TEST_DATA["manufacturer1"])

    def setUp(self):
        self.manufacturer = Manufacturer.objects.first()

    def test_manufacturer_ordering_by_name_field(self):
        ordering = self.manufacturer._meta.ordering
        expected_ordering = ["name", ]
        self.assertEqual(ordering[0], expected_ordering[0])

    def test_object_name_is_name_and_country(self):
        expected_object_name = (
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
        self.assertEqual(str(self.manufacturer), expected_object_name)
