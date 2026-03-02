from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car

User = get_user_model()


class ManufacturerModelTests(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.assertEqual(
            str(manufacturer),
            "Toyota Japan"
        )

    def test_ordering(self):
        m1 = Manufacturer.objects.create(name="BMW", country="Germany")
        m2 = Manufacturer.objects.create(name="Audi", country="Germany")

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(manufacturers),
            [m2, m1]
        )

