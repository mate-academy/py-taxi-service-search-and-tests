from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTestCase(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    # def test_driver_str(self):
    #     # f"{self.username} ({self.first_name} {self.last_name})"
    #     driver = get_user_model().objects.create(
    #         username="TestName",
    #         password="TestPassword12345",
    #         first_name="TestFirstName",
    #     )