from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="securepassword123"
        )
        self.client.force_login(self.user)

        self.driver_1 = get_user_model().objects.create_user(
            username="test1_driver",
            password="pwd",
            license_number="AAA11111"
        )
        self.driver_2 = get_user_model().objects.create_user(
            username="test2_driver",
            password="pwd",
            license_number="BBB22222"
        )

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car_1 = Car.objects.create(
            model="model1",
            manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="model2",
            manufacturer=self.manufacturer_2
        )

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {"username": "test1_driver"})
        self.assertContains(response, "test1_driver")
        self.assertNotContains(response, "test2_driver")

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "model1"})
        self.assertContains(response, "model1")
        self.assertNotContains(response, "model2")

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "Toyota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
