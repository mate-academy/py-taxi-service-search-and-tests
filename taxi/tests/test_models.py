from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")
        self.assertEqual(manufacturers[2].name, "Tesla")


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "john (John Smith)"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver.pk},
            ),
        )

    def test_driver_verbose_name(self):
        self.assertEqual(
            Driver._meta.verbose_name,
            "driver",
        )

    def test_driver_verbose_name_plural(self):
        self.assertEqual(
            Driver._meta.verbose_name_plural,
            "drivers",
        )


class CarModelTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "X5")
