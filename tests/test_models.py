from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer_instance = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.car_instance = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer_instance
        )
        self.driver_instance = Driver.objects.create(
            username="test_username",
            password="<PASSWORD>",
            license_number="ABC12345",
            first_name="test_first_name",
            last_name="test_last_name",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer_instance),
            "test_name test_country"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver_instance),
            "test_username (test_first_name test_last_name)"
        )

    def test_driver_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver_instance.id}
        )

        self.assertEqual(
            self.driver_instance.get_absolute_url(),
            expected_url
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car_instance),
            "test_model"
        )
