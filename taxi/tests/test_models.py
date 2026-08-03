from django.test import TestCase

from taxi.models import Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_name(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", country="USA")
        self.assertEqual(f"{manufacturer.name} {manufacturer.country}", str(manufacturer))
