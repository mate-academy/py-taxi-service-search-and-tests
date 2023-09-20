from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Volkswagen", country="Germany")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)

    def test_manufacturer_queryset_ordered_by_name_asc(self):
        manufacturer_1 = Manufacturer.objects.get(id=1)
        manufacturer_2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        queryset = Manufacturer.objects.all()

        self.assertEqual(queryset[0], manufacturer_2)
        self.assertEqual(queryset[1], manufacturer_1)


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "TestUser",
            "password": "test123user",
            "first_name": "John",
            "last_name": "Doe"
        }

    def test_creating_driver_with_license_number(self):
        self.user_data["license_number"] = "Test1234"
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.license_number, self.user_data["license_number"])

    def test_driver_str(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(
            str(user),
            f"{user.username} ({user.first_name} {user.last_name})"
        )

    def test_driver_get_absolute_url(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(
            user.get_absolute_url(),
            reverse("taxi:driver-detail", args=[user.id])
        )


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        car = Car.objects.create(
            model="Volkswagen Tiguan",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
