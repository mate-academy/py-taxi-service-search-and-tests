from django.test import TestCase

from taxi.models import Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine"
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
