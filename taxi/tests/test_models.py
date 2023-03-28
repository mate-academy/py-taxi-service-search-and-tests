from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="little_ann",
            password="12345",
            license_number="AAA12345",
            first_name="Anna",
            last_name="Kass"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Germany"
        )
        car = Car.objects.create(model="Gimlet", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.get(username="little_ann")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_license_number_is_unique(self):
        driver = get_user_model().objects.get(username="little_ann")
        is_unique = driver._meta.get_field("license_number").unique
        self.assertEqual(is_unique, True)
