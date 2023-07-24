from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Driver, Manufacturer


class DriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC123",
        )

    def test_driver_str_method(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_driver_verbose_names(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")


class CarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )

    def test_car_str_method(self):
        self.assertEqual(str(self.car), self.car.model)


class ManufacturerModelTest(TestCase):
    def setUp(self):
        data = {
            ("Test Manufacturer", "Test Country"),
            ("Apple", "USA"),
            ("Samsung", "South Korea"),
        }
        for name, country in data:
            Manufacturer.objects.create(name=name, country=country)

    def test_manufacturer_str_method(self):
        manufacturers = Manufacturer.objects.all()
        for manufacturer in manufacturers:
            expected_str = f"{manufacturer.name} {manufacturer.country}"
            self.assertEqual(str(manufacturer), expected_str)

    def test_manufacturer_ordering(self):
        manufacturers_by_name = list(
            Manufacturer.objects.values_list("name", flat=True)
        )
        self.assertEqual(
            manufacturers_by_name, ["Apple", "Samsung", "Test Manufacturer"]
        )
