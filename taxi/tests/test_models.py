from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ManufacturerModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )

    def test_manufacturer_name_max_length(self) -> None:
        max_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_country_max_length(self) -> None:
        max_length = self.manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_object_name_is_name_and_country_in_parentheses(
        self,
    ) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} ({self.manufacturer.country})",
        )


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="test_username",
            password="test_password",
            license_number="ABC12345",
        )

    def test_driver_license_number_max_length(self) -> None:
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)


class CarModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

    def test_car_model_max_length(self) -> None:
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)
