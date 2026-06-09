from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestStrFuncOfModels(TestCase):
    def test_manufacturer_str(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )
        self.assertEqual(str(new_manufacturer), "Test Test country")

    def test_driver_str(self):
        new_driver = Driver.objects.create(
            license_number="ASD12345",
            first_name="Test name",
            last_name="Test last name",
            username="Test username",
        )
        self.assertEqual(
            str(new_driver),
            "Test username (Test name Test last name)"
        )

    def test_car_str(self):
        new_car = Car.objects.create(
            model="Test model",
            manufacturer=Manufacturer.objects.create(
                name="Test",
                country="Test country",
            ),
        )
        self.assertEqual(str(new_car), "Test model")
