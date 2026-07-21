from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="user",
            password="testuser",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)

    def test_manufacturer_str(self):

        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):

        self.assertEqual(
            str(self.car),
            f"{self.car.model}"
        )

    def test_user_str(self):

        self.assertEqual(
            str(self.user),
            f"{self.user.username} "
            f"({self.user.first_name} {self.user.last_name})"
        )

    def test_get_absolute_url_user(self):

        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.user.pk}
        )

        self.assertEqual(
            self.user.get_absolute_url(),
            expected_url
        )

    def test_create_user_with_license_number(self):

        user1 = get_user_model().objects.create_user(
            username="user1",
            password="testuser",
            license_number="TES12345"
        )

        self.assertEqual(
            user1.license_number,
            "TES12345"
        )
