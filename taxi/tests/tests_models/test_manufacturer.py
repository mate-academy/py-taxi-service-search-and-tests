from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_name_label(self):
        field_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        field_label = self.manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        max_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        max_length = self.manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        try:
            Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
            assert False
        except IntegrityError:
            assert True

    def test_manufacturer_str(self):
        expected_str = f"{self.manufacturer.name} {self.manufacturer.country}"
        self.assertEqual(expected_str, str(self.manufacturer))
