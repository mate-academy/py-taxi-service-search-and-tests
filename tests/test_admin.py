from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class AdminTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="jon.doe",
            first_name="John",
            last_name="Doe",
            email="john@taxi.com",
            license_number="ABC12345"
        )

    def test_driver_license_number_field(self):
        self.assertEqual(self.driver.license_number, "ABC12345")
        self.driver.save()
        self.assertTrue(get_user_model().objects.filter(
            license_number="ABC12345").exists())

    def test_car_custom_fields(self):
        self.assertEqual(self.car.model, "Camry")
        self.assertEqual(self.car.manufacturer.name, "Toyota")
        self.car.save()
        self.assertTrue(Car.objects.filter(model="Camry").exists())
        self.assertTrue(Manufacturer.objects.filter(name="Toyota").exists())
