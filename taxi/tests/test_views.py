from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="driver",
            password="test123!",
            license_number="DVR00001",
        )
        self.client.force_login(self.driver)

        self.tesla = Manufacturer.objects.create(name="Tesla", country="USA")
        self.land_rover = Manufacturer.objects.create(
            name="Land Rover",
            country="United Kingdom"
        )

        self.tesla_s = Car.objects.create(
            model="Tesla S",
            manufacturer=self.tesla
        )
        self.tesla_x = Car.objects.create(
            model="Tesla X",
            manufacturer=self.tesla
        )
        self.range_rover = Car.objects.create(
            model="Range Rover",
            manufacturer=self.land_rover
        )

        self.url = reverse("taxi:car-list")

    def test_car_list_search_by_model(self):
        response = self.client.get(self.url, data={"model": "Tesla"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tesla_s, response.context["car_list"])
        self.assertIn(self.tesla_x, response.context["car_list"])
        self.assertNotIn(self.range_rover, response.context["car_list"])

    def test_car_list_search_exact_match(self):
        response = self.client.get(self.url, data={"model": "Range Rover"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.range_rover, response.context["car_list"])
        self.assertNotIn(self.tesla_s, response.context["car_list"])
        self.assertNotIn(self.tesla_x, response.context["car_list"])


class DriverListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.auth_user = get_user_model().objects.create(
            username="main",
            password="test123!",
            license_number="DVR00001",
        )
        self.client.force_login(self.auth_user)

        self.ross = get_user_model().objects.create(
            username="ross",
            password="test123!",
            license_number="DVR00002",
        )
        self.rachel = get_user_model().objects.create(
            username="rachel",
            password="test123!",
            license_number="DVR00003",
        )
        self.monika = get_user_model().objects.create(
            username="monika",
            password="test123!",
            license_number="DVR00004",
        )
        self.url = reverse("taxi:driver-list")

    def test_driver_list_search_by_username(self):
        response = self.client.get(self.url, data={"username": "r"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.ross, response.context["driver_list"])
        self.assertIn(self.rachel, response.context["driver_list"])
        self.assertNotIn(self.monika, response.context["driver_list"])

    def test_driver_list_exact_match(self):
        response = self.client.get(self.url, data={"username": "ross"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.ross, response.context["driver_list"])
        self.assertNotIn(self.rachel, response.context["driver_list"])
        self.assertNotIn(self.monika, response.context["driver_list"])


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="main",
            password="test1234!",
            license_number="DVR0001",
        )
        self.client.force_login(self.user)
        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.bugatti = Manufacturer.objects.create(
            name="Bugatti",
            country="France"
        )
        self.land_rover = Manufacturer.objects.create(
            name="Land Rover",
            country="United Kingdom"
        )
        self.url = reverse("taxi:manufacturer-list")

    def test_manufacturer_list_search_by_model(self):
        response = self.client.get(self.url, data={"name": "b"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.bmw, response.context["manufacturer_list"])
        self.assertIn(self.bugatti, response.context["manufacturer_list"])
        self.assertNotIn(
            self.land_rover,
            response.context["manufacturer_list"]
        )

    def test_manufacturer_list_exact_match(self):
        response = self.client.get(self.url, data={"name": "Land Rover"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.land_rover, response.context["manufacturer_list"])
        self.assertNotIn(self.bmw, response.context["manufacturer_list"])
        self.assertNotIn(self.bugatti, response.context["manufacturer_list"])
