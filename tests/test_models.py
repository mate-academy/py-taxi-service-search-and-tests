from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "BMW")
        self.assertEqual(manufacturers[1].name, "Toyota")


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="admin_user",
            password="87ASDHADIK7asd7IA6SD",
            first_name="Mike",
            last_name="Smith",
            license_number="AAA1111",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver), "admin_user (Mike Smith)"
        )

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        kwargs = {"pk": self.driver.pk}
        expected_url = reverse(
            "taxi:driver-detail", kwargs=kwargs
        )
        self.assertEqual(url, expected_url)


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_car_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)
