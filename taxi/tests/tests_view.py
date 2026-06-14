from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class PrivateSearchTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="main_driver",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturer_list)
        self.assertNotIn(self.manufacturer2, manufacturer_list)

    def test_search_car_by_model(self):
        car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cam"})
        car_list = response.context["car_list"]

        self.assertIn(car1, car_list)
        self.assertNotIn(car2, car_list)

    def test_search_driver_by_username(self):
        other_driver = get_user_model().objects.create_user(
            username="alex_taxi",
            password="password123",
            license_number="BBB22222"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "alex"})
        driver_list = response.context["driver_list"]

        self.assertIn(other_driver, driver_list)
        self.assertNotIn(self.user, driver_list)
