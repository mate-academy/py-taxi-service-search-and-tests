from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchDriver(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "pass123",
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        form = {
            "username": "test",
        }
        get_user_model().objects.create(
            username="driver", license_number="TES12345"
        )
        filtered_drivers = get_user_model().objects.filter(
            username__icontains=form["username"]
        )
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=" + form["username"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]), list(filtered_drivers)
        )


class SearchManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "pass123",
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        form = {
            "manufacturer": "test",
        }
        filtered_manufacturers = Manufacturer.objects.filter(
            name__icontains=form["manufacturer"]
        )
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list"
            ) + "?manufacturer=" + form["manufacturer"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ),
            list(filtered_manufacturers)
        )


class SearchCars(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "pass123",
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        form = {
            "car_model": "test",
        }
        filtered_cars = Car.objects.filter(model__icontains=form["car_model"])
        response = self.client.get(
            reverse(
                "taxi:car-list"
            ) + "?car_model=" + form["car_model"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(filtered_cars)
        )
