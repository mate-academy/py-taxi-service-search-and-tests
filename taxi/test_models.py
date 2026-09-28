from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class ManufacturerModelTest(TestCase):
    def test_string_representation(self):
        manufacturer = Manufacturer(name="Toyota", country="Japan")

        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_manufacturers_are_ordered_by_name(self):
        Manufacturer.objects.create(name="Volvo", country="Sweden")
        Manufacturer.objects.create(name="Audi", country="Germany")

        manufacturers = list(Manufacturer.objects.all())

        self.assertEqual(
            manufacturers,
            [
                Manufacturer.objects.get(name="Audi"),
                Manufacturer.objects.get(name="Volvo"),
            ],
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="alex",
            password="testpass123",
            license_number="ABC12345",
            first_name="Alex",
            last_name="Smith",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.driver), "alex (Alex Smith)")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.car = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.car), "Camry")
