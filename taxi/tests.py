from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver


# Create your tests here.
class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")


class ManufacturerSearchListViewTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="toyota", country="japan")
        Manufacturer.objects.create(name="ford", country="usa")
        Manufacturer.objects.create(name="bmw", country="germany")

    def test_query_search_filter(self):
        self.assertQuerysetEqual((Manufacturer.
                                  objects.
                                  filter(name__icontains="ford").
                                  values("name", "country")),
                                 [{"name": "ford", "country": "usa"}])

    def test_query_search_toyota(self):
        self.assertQuerysetEqual((Manufacturer.
                                  objects.
                                  filter(name__icontains="toyota").
                                  values("name", "country")),
                                 [{"name": "toyota", "country": "japan"}])

    def test_query_search_with_o(self):
        self.assertQuerysetEqual((Manufacturer.
                                  objects.
                                  filter(name__icontains="o").
                                  values("name", "country")),
                                 [{"name": "ford", "country": "usa"},
                                  {"name": "toyota", "country": "japan"}])
