from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="teste",
            password="Adm12345",
            first_name="Test",
            last_name="Tes"
        )
        self.client.force_login(self.user)

        self.manufacturer_test = Manufacturer.objects.create(
            name="Test", country="Teste")
        self.manufacturer_bmw = Manufacturer.objects.create(
            name="BMW", country="Teste")

    def test_search_form(self):
        form_data = {"name": "Test"}
        response = self.client.get(MANUFACTURER_URL, data=form_data)

        self.assertEqual(response.status_code, 200)

        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer_test, manufacturer_list)
        self.assertNotIn(self.manufacturer_bmw, manufacturer_list)

    def test_search_empty_returns_all(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            2
        )


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="teste",
            password="Adm12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car_match = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

        self.car_no_match = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            CAR_URL,
            {"model": "X5"}
        )

        self.assertEqual(response.status_code, 200)

        car_list = response.context["car_list"]

        self.assertIn(self.car_match, car_list)
        self.assertNotIn(self.car_no_match, car_list)

    def test_search_empty_returns_all(self):
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["car_list"]),
            2
        )

    def test_search_form_in_context(self):
        response = self.client.get(CAR_URL)

        self.assertIn("search_form", response.context)


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="Adm12345",
            license_number="LIC-000"
        )
        self.client.force_login(self.user)

        self.driver_match = get_user_model().objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="LIC-001"
        )

        self.driver_no_match = get_user_model().objects.create_user(
            username="maria_silva",
            password="test12345",
            license_number="LIC-002"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            DRIVER_URL,
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        driver_list = response.context["driver_list"]

        self.assertIn(self.driver_match, driver_list)
        self.assertNotIn(self.driver_no_match, driver_list)

    def test_search_empty_returns_all(self):
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["driver_list"]),
            3  # admin + 2 drivers
        )

    def test_search_form_in_context(self):
        response = self.client.get(DRIVER_URL)

        self.assertIn("search_form", response.context)
