from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer
        )

        cls.driver = get_user_model().objects.create_user(
            username="test",
            password="t5st_P@ss",
            first_name="testus",
            last_name="testenko",
            license_number="TES77587"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "test test_country"
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            "test_model"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "test (testus testenko)"
        )

    def test_create_driver_with_license(self):
        self.assertEqual(
            self.driver.license_number,
            "TES77587"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver.pk}
            )
        )
