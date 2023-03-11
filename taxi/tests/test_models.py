from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self) -> None:
        self.b_manufacturer = Manufacturer.objects.create(
            name="b",
            country="Japan"
        )
        self.a_manufacturer = Manufacturer.objects.create(
            name="a",
            country="Germany"
        )

    def test_str(self):

        self.assertEqual(
            str(self.a_manufacturer), f"{self.a_manufacturer.name} "
                                      f"{self.a_manufacturer.country}"
        )

    def test_ordering(self):

        self.assertEqual(Manufacturer.objects.all()[0], self.a_manufacturer)
        self.assertEqual(Manufacturer.objects.all()[1], self.b_manufacturer)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="ace_ventura",
            password="test12345",
            license_number="AAA00000"
        )

    def test_str(self):

        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ("
            f"{self.driver.first_name} {self.driver.last_name})"
        )

    def test_absolute_url(self):

        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

    def test_str(self):

        self.assertEqual(str(self.car), "test_model")
