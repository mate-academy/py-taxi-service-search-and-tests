from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):

    def test_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.assertEqual(f"{manufacturer}", "test_name test_country")


class DriverTest(TestCase):

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password",
            license_number="ADM56984",
            first_name="fist_name",
            last_name="last_name"
        )

    def test_str_method(self) -> None:

        self.assertEqual(
            f"{self.driver}", "test_driver (fist_name last_name)"
        )

    def test_license_number_present(self) -> None:
        self.assertEqual(self.driver.license_number, "ADM56984")


class CarTest(TestCase):

    def test_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(f"{car}", "test_model")
