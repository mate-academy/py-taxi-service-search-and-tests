from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )
        self.driver = get_user_model().objects.create(
            username="test_username",
            password="<PASSWORD>",
            first_name="first",
            last_name="last"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )

    def test_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "Test Manufacturer United States"
        )
        self.assertEqual(str(self.driver), "test_username (first last)")
        self.assertEqual(str(self.car), "Test Model")
