from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_str_methods(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer)

        self.assertEqual(
            str(manufacturer),
            "test Test",
            "Check str method for manufacturer"
        )
        self.assertEqual(
            str(car),
            car.model,
            "Check str method for car model"
        )

    def test_invalid_license_lowercase(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="123qwer456",
            license_number="asd12345"
        )
        self.assertFalse(
            user.license_number[:3].isupper(),
            msg="First 3 characters should be uppercase letters"
        )

    def test_invalid_license_len(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="123qwer456",
            license_number="ASD12345678"
        )
        self.assertTrue(
            len(user.license_number) != 8,
            msg="Drivers license should be 8 characters long"
        )

    def test_invalid_license_not_num(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="123qwer456",
            license_number="ASD1234a"
        )
        self.assertFalse(
            user.license_number[3:].isdigit(),
            msg="Drivers license should be with 5 digits"
        )
