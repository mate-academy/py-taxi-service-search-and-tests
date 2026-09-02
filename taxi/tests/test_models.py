from django.test import TestCase

from taxi.models import Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(
            name="Toyota",
            country="Japan"
        )

        self.assertEqual(
            str(manufacturer),
            "Toyota Japan"
        )
