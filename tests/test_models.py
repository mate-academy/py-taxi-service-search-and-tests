from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car

User = get_user_model()


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany")

    def test_name_field_label(self):
        field_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_field_max_length(self):
        max_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_field_unique(self):
        is_unique = self.manufacturer._meta.get_field("name").unique
        self.assertTrue(is_unique)

    def test_object_str_returns_name_plus_country(self):
        self.assertEqual(str(self.manufacturer), "Audi Germany")

    def test_ordering(self):
        self.assertEqual(self.manufacturer._meta.ordering, ["name"])


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = User.objects.create_user(
            username="testdriver",
            password="testpass123",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345",
        )

    def test_license_number_unique(self):
        is_unique = self.driver._meta.get_field("license_number").unique
        self.assertTrue(is_unique)

    def test_license_number_max_length(self):
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "testdriver (John Smith)")

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertEqual(
            url, reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany")
        cls.car = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "X5")

    def test_drivers_many_to_many(self):
        self.assertEqual(self.car.drivers.count(), 0)
