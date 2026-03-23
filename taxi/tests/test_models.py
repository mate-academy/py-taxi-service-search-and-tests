from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from taxi.models import Car, Manufacturer, Driver


class ManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Zebra",
            country="Country"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Aple",
            country="Country"
        )
        self.manufacturer_3 = Manufacturer.objects.create(
            name="Frd",
            country="Country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Test Country")

    def test_name_manufacturer_order(self):
        manufacturers = Manufacturer.objects.all()
        manufacturers_names = [
            manufacturer.name for manufacturer in manufacturers
        ]
        self.assertEqual(manufacturers_names, ["Aple", "Frd", "Test", "Zebra"])


class CarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )

    def test_car_string(self):
        self.assertEqual(str(self.car), "TestModel")

    def test_car_delete_manufacturer(self):
        self.manufacturer.delete()
        cars = Car.objects.all()
        self.assertEqual(cars.count(), 0)


class DriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
            license_number="PKL99881",
            first_name="Test_first_name",
            last_name="Test_last_name"
        )

    def test_get_absolute_url_method(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.pk}
                    )
        )

    def test_unique_driver(self):

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="TestUser1",
                password="Password1",
                license_number="PKL99881",
            )
