from django.test import TestCase
from taxi.models import Manufacturer


class ManufacturerModelTest(TestCase):
    def test_str_returns_name(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.assertEqual(str(manufacturer), "Tesla")
