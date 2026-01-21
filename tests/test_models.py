from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


# Create your tests here.

class ModelTests(TestCase):

    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(name="Test",
                                                   country="Test")

        self.assertEqual(str(manufacturer), manufacturer.__str__())

    def test_driver_format_str(self):
        username = "Vasyl2hardforYou"
        first_name = "Vasyl"
        last_name = "Nenko"
        driver = get_user_model().objects.create(username=username,
                                                 first_name=first_name,
                                                 last_name=last_name)

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")
