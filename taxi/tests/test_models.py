from django.test import TestCase

from taxi.models import Manufacturer


class ManufacturerModelTests(TestCase):
    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.assertEqual(manufacturer.name, "Test Manufacturer")
        self.assertEqual(manufacturer.country, "Test Country")
