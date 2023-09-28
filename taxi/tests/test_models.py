from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test user",
            first_name="test first_name",
            last_name="test last_name",
            password="testuser",
            license_number="ABC12345",
        )

    def test_manufacturer_and_car_correct_str_display(self):
        manufacturer = Manufacturer.objects.create(
            name="test name", country="test country"
        )
        self.assertEqual(str(manufacturer), "test name test country")

        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), "test model")

    def test_driver_correct_str_display(self):
        self.assertEqual(
            str(self.driver), "test user (test first_name test last_name)"
        )

    def test_driver_correct_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )
