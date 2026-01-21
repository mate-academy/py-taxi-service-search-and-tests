from django.test import TestCase

from taxi.models import Manufacturer, Car
from taxi.tests import fixtures


class ManufacturerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_object_to_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_query_set_should_be_ordered_by_name(self):
        unordered_names = ["Cab", "Abc", "Bca"]
        for name in unordered_names:
            Manufacturer.objects.create(name=name, country="country")
        names = [
            manufacturer.name
            for manufacturer in Manufacturer.objects.all()[:3]
        ]

        self.assertEqual(names, ["Abc", "Bca", "Cab"])

    def test_name_field_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length

        self.assertEqual(max_length, 255)

    def test_country_field_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length

        self.assertEqual(max_length, 255)
