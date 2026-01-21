from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarListTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC76594",
        )
        self.client.login(username="test111", password="paSS1ord")
        car = Car.objects.create(
            model="CBR-1000",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

    def test_get_queryset_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "CBR-1000")

    def test_get_context_data_car_list_view(self):
        response = self.client.get(reverse(
            "taxi:car-list"),
            {"search": "CBR-1000"}
        )
        self.assertIn("search_form", response.context)


class ManufacturerListTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC76594",
        )
        self.client.login(username="test111", password="paSS1ord")

    def test_get_queryset_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Ferrari")

    def test_get_context_data_manufacturer_list_view(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"search": "Ferrari"}
        )
        self.assertIn("search_form", response.context)


class DriverListTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC76594",
        )
        self.client.login(username="test111", password="paSS1ord")

    def test_get_queryset_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "test111")
