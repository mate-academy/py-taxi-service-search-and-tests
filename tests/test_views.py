from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class TestSearchViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")

        Car.objects.create(model="TestCar1", manufacturer=manufacturer)
        Car.objects.create(model="TestCar2", manufacturer=manufacturer)
        Car.objects.create(model="TestCar12", manufacturer=manufacturer)

        response = self.client.get(CAR_URL, {"model": "2"})
        queryset = response.context["object_list"]

        self.assertEqual(len(queryset), 2)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="TestManufacturer1",
            country="TestCountry"
        )
        Manufacturer.objects.create(
            name="TestManufacturer2",
            country="TestCountry"
        )
        Manufacturer.objects.create(
            name="TestManufacturer12",
            country="TestCountry"
        )

        response = self.client.get(MANUFACTURER_URL, {"name": "2"})
        queryset = response.context["object_list"]

        self.assertEqual(len(queryset), 2)

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="TestUser1",
            password="TestPassword1",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="TestUser2",
            password="TestPassword2",
            license_number="TES12346"
        )
        get_user_model().objects.create_user(
            username="TestUser12",
            password="TestPassword12",
            license_number="TES12347"
        )
        response = self.client.get(DRIVER_URL, {"username": "2"})
        queryset = response.context["object_list"]

        self.assertEqual(len(queryset), 2)
