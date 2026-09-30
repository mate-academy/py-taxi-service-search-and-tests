from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer, model="Yaris"
        )
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="1234testpass",
            first_name="Admin",
            last_name="Adminovich",
        )
        self.client.force_login(self.user)

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Yaris")

    def test_user_str(self):
        self.assertEqual(str(self.user), "admin (Admin Adminovich)")
