from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicViewTests(TestCase):

    def test_login_required_for_lists(self):
        urls = [DRIVER_LIST_URL, CAR_LIST_URL, MANUFACTURER_LIST_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateSearchTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="password123",
            license_number="AAA12345"
        )
        self.client.force_login(self.driver)

        # Sample data for searching
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car_1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer_2
        )

        self.driver_2 = get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="BBB12345"
        )

    # --- Manufacturer Search Tests ---
    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toy"})
        self.assertContains(response, self.manufacturer_1.name)
        self.assertNotContains(response, self.manufacturer_2.name)

    def test_search_manufacturer_case_insensitive(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "toyota"})
        self.assertContains(response, self.manufacturer_1.name)

    # --- Car Search Tests ---
    def test_search_car_by_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Cam"})
        self.assertContains(response, self.car_1.model)
        self.assertNotContains(response, self.car_2.model)

    # --- Driver Search Tests ---
    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        drivers_in_context = response.context["driver_list"]
        self.assertIn(self.driver_2, drivers_in_context)
        self.assertNotIn(self.driver, drivers_in_context)
