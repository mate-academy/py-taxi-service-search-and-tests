from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_str_method(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_unique_name(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Toyota", country="USA")


class DriverModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="AB123456"
        )

    def test_str_method(self):
        self.assertEqual(str(self.driver), "john_doe (John Doe)")

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        ))

    def test_unique_license_number(self):
        with self.assertRaises(Exception):
            Driver.objects.create(
                username="jim_doe",
                first_name="Jim",
                last_name="Doe",
                license_number="AB123456"
            )


class CarModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.car = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer
        )
        cls.driver1 = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="AB123456"
        )
        cls.driver2 = Driver.objects.create(
            username="jane_doe",
            first_name="Jane",
            last_name="Doe",
            license_number="XY789012"
        )
        cls.car.drivers.add(cls.driver1, cls.driver2)

    def test_str_method(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_car_driver_relationship(self):
        self.assertIn(self.driver1, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())

    def test_manufacturer_foreign_key(self):
        manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car.manufacturer = manufacturer2
        self.car.save()
        self.assertEqual(self.car.manufacturer, manufacturer2)
