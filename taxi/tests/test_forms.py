from django.contrib.auth import get_user_model
from django.test import TestCase
from .test_views import (MANUFACTURER_URl, CAR_URL,
                         DRIVER_URL)
from ..models import Manufacturer, Car


class SearchManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer(self) -> None:
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BWM", country="Germany")
        Manufacturer.objects.create(name="Toyota land cruiser",
                                    country="Japan")
        response = self.client.get(MANUFACTURER_URl, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.filter(name__icontains="Toyota")
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers)
                         )


class SearchCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="password"
        )
        self.client.force_login(self.user)

    def test_search_car(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Test",
                                                   country="Japan")
        Car.objects.create(model="BWM M5", manufacturer=manufacturer)
        Car.objects.create(model="BWM M3", manufacturer=manufacturer)
        Car.objects.create(model="Toyota", manufacturer=manufacturer)
        response = self.client.get(CAR_URL, {"model": "BWM"})
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.filter(model__icontains="BWM")
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))


class SearchDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_driver(self) -> None:
        get_user_model().objects.create_user(
            username="John",
            password="password123",
            license_number="ABG44156"
        )
        get_user_model().objects.create_user(
            username="Nazar",
            password="Nazar6661",
            license_number="AAC44226"
        )
        get_user_model().objects.create_user(
            username="John12",
            password="johnemail123",
            license_number="ABC44556"
        )
        response = self.client.get(DRIVER_URL, {"username": "John"})
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.filter(username__icontains="John")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
