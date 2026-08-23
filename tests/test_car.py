from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="user1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        self.car1 = Car.objects.create(
            model="Audi a4",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer,
        )

    def test_search_by_car_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Audi"})
        car_list = response.context["car_list"]

        self.assertTrue(self.car1 in car_list)
        self.assertFalse(self.car2 in car_list)

    def test_search_car_is_case_insensitive(self):
        response = self.client.get(CAR_LIST_URL, {"model": "audi"})
        car_list = response.context["car_list"]

        self.assertTrue(self.car1 in car_list)

    def test_empty_return_search_field(self):
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 2)
