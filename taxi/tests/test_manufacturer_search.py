from django.test import TestCase
from taxi.models import Manufacturer


class ManufacturerSearchTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.manufacturer3 = Manufacturer.objects.create(
            name="TestFabricators",
            country="Germany"
        )

    def test_search_manufacturer_by_name_existing(self):
        results = Manufacturer.objects.filter(name__icontains="Tes")
        self.assertEqual(len(results), 2)
        self.assertIn(self.manufacturer1, results)

    def test_search_manufacturer_by_name_partial(self):
        results = Manufacturer.objects.filter(name__icontains="Test")
        self.assertEqual(len(results), 1)  # "Tesla" и "TestFabricators"
        self.assertIn(self.manufacturer3, results)

    def test_search_manufacturer_non_existing(self):

        results = Manufacturer.objects.filter(name__icontains="NonExistent")
        self.assertEqual(len(results), 0)
