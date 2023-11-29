from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name ", country="test_country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        user = get_user_model().objects.create(
            username="test_user",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="test_license_number",
        )
        self.assertEqual(
            str(user), f"{user.username} {user.first_name} {user.last_name}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")
