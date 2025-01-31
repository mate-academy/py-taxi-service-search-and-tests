from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

        self.driver = get_user_model().objects.create_user(
            username="test.username",
            password="pasword123",
            first_name="TestF",
            last_name="TestL",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_model_name(self):
        self.assertEqual(
            str(self.manufacturer),
            "Test Manufacturer Test Country"
        )
        self.assertEqual(
            str(self.driver),
            "test.username (TestF TestL)"
        )
        self.assertEqual(str(self.car), "Test Model")
