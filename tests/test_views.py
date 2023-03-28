from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class UserCarManufacturer:
    def generate_data(self):
        self.user = get_user_model().objects.create(
            username="test_user",
            password="test24152",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Acura",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="MDX",
            manufacturer=self.manufacturer
        )


class NotLoginCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class LoginCarListTest(TestCase, UserCarManufacturer):
    def setUp(self) -> None:
        self.generate_data()
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
