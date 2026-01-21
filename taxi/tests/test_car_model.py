from django.db import models
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver
from taxi.tests import fixtures


class CarModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), car.model)

    def test_model_field_max_length(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("model").max_length

        self.assertEqual(max_length, 255)

    def test_manufacturer_field(self):
        field = Car._meta.get_field("manufacturer")

        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.related_model, Manufacturer)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_drivers_field(self):
        field = Car._meta.get_field("drivers")

        self.assertTrue(isinstance(field, models.ManyToManyField))
        self.assertEqual(field.related_model, Driver)
        self.assertEqual(field.remote_field.related_name, "cars")
