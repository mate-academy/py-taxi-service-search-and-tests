from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_string_return(self):
        obj = Manufacturer.objects.create()
        self.assertEqual(
            str(obj),
            f"{obj.name} {obj.country}"
        )

    def test_driver_string_return(self):
        obj = Driver.objects.create()
        self.assertEqual(
            str(obj),
            f"{obj.username} ({obj.first_name} {obj.last_name})"
        )

    def test_car_string_return(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        obj = Car.objects.create(manufacturer=manufacturer)
        self.assertEqual(
            str(obj),
            obj.model
        )
