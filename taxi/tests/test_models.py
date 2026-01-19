from django.test import TestCase
from taxi.models import Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany"
                                                   )
        self.assertEqual(str(manufacturer), "BMW Germany")
