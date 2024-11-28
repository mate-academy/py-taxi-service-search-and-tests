from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testmate", password="1234"
        )
        self.client.login(username="testmate", password="1234")

        # filling database with test data
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer")
        self.car = Car.objects.create(
            model="test_car", manufacturer=self.manufacturer)
        self.driver = Driver.objects.create(
            username="test_driver", license_number="QWE12345")

    def test_search_cars(self):
        response = self.client.get(reverse("taxi:search-cars"), {"q": "car"})
        self.assertContains(response, "test_car")

    def test_search_drivers(self):
        response = self.client.get(
            reverse("taxi:search-drivers"), {"q": "driver"})
        self.assertContains(response, "test_driver")

    def test_search_manufacturers(self):
        response = self.client.get(
            reverse("taxi:search-manufacturers"), {"q": "manufacturer"})
        self.assertContains(response, "test_manufacturer")
