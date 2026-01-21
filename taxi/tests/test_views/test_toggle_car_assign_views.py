from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car
from taxi.tests.test_views.initial_data import (
    TOGGLE_URL,
    CAR_DETAIL_URL
)


class ToggleCarAssignTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.client.force_login(self.user)

    def test_assign_driver_to_car(self):
        self.client.get(TOGGLE_URL)
        self.assertTrue(self.car in self.user.cars.all())

    def test_unassign_driver_from_car(self):
        self.car.drivers.add(self.user)
        self.client.get(TOGGLE_URL)
        self.assertFalse(self.car in self.user.cars.all())

    def test_redirect_to_car_detail_page(self):
        response = self.client.get(TOGGLE_URL)
        self.assertRedirects(response, CAR_DETAIL_URL)
