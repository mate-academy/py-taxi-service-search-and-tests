from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test12345"
        )
        self.client.force_login(self.user)
        self.urls = {
            "manufacturer": reverse("taxi:manufacturer-list"),
            "car": reverse("taxi:car-list"),
            "driver": reverse("taxi:driver-list"),
        }

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="TestCountry1",
            country="Test Country1"
        )
        Manufacturer.objects.create(
            name="TestCountry2",
            country="Test Country2"
        )
        Manufacturer.objects.create(
            name="QWERTY",
            country="QWERTY Country"
        )

        url = f"{self.urls['manufacturer']}?name=Test"
        response = self.client.get(url)
        queryset_from_response = response.context["manufacturer_list"]
        valid_queryset = Manufacturer.objects.filter(name__icontains="Test")

        self.assertEqual(
            list(queryset_from_response),
            list(valid_queryset),
        )

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="TestCountry1",
            country="Test Country1"
        )
        Car.objects.create(
            model="TestModel1",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="TestModel2",
            manufacturer=manufacturer
        )

        url = f"{self.urls['car']}?car_model=Test"
        response = self.client.get(url)
        queryset_from_response = response.context["car_list"]
        valid_queryset = Car.objects.filter(model__icontains="Test")

        self.assertEqual(
            list(queryset_from_response),
            list(valid_queryset),
        )

    def test_search_driver(self):
        Driver.objects.create_user(
            username="TestUser1",
            password="Test12345",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="TestUser2",
            password="Test54321",
            license_number="ABC54321"
        )

        url = f"{self.urls['driver']}?username=Test"
        response = self.client.get(url)
        queryset_from_response = response.context["driver_list"]
        valid_queryset = Driver.objects.filter(username__icontains="Test")

        self.assertEqual(
            list(queryset_from_response),
            list(valid_queryset),
        )
