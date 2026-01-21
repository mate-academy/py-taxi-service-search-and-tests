from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer
from django.test import TestCase


class ManufacturerModelTest(TestCase):
    def test_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Saab",
            counry="Sweden",
        )
        self.assertEqual(str(manufacturer), "Saab Sweden")


class CarModelTest(TestCase):
    def test_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Saab",
            counry="Sweden",
        )
        car = Car.objects.create(
            model="9-5",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "9-5")


class DriverModelTest(TestCase):
    def test_str_method(self) -> None:
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword4545",
            first_name="testfirstname",
            last_name="testlastname",
            license_number="TST12345"
        )
        self.assertEqual(str(user), "testuser(testfirstname testlastname)")
