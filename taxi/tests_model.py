from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTestCase(TestCase):

    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW Group",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car(self):
        manufacturer = Manufacturer.objects.create(name="BMW Group")
        car = Car.objects.create(model="BMW", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
