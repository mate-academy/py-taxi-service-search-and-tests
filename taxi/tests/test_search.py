from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Car, Driver

car_url = reverse("taxi:car-list")
driver_url = reverse("taxi:driver-list")
manufacturer_url = reverse("taxi:manufacturer-list")


class CarListViewSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test-user",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="BMW")
        self.car1 = Car.objects.create(
            model="E60",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="E61",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="E31",
            manufacturer=self.manufacturer
        )

    def test_search_form_in_context(self):
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_search_form_no_results(self):
        response = self.client.get(car_url, {"model": "Unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["object_list"],
            []
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver1 = Driver.objects.create_user(
            username="john_doe",
            password="password123",
            license_number="12345678-test",
        )
        self.client.force_login(self.driver1)
        self.driver2 = Driver.objects.create_user(
            username="jane_smith",
            password="password123",
            license_number="1272658-test",
        )
        self.client.force_login(self.driver2)
        self.driver3 = Driver.objects.create_user(
            username="john_smith",
            password="password123",
            license_number="365856-test",
        )
        self.client.force_login(self.driver3)

    def test_search_form_in_context(self):
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )

    def test_queryset_no_results(self):
        response = self.client.get(driver_url, {"username": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["object_list"],
            []
        )


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford")
        self.manufacturer3 = Manufacturer.objects.create(name="BMW")

    def test_search_form_in_context(self):
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )

    def test_queryset_no_results(self):
        response = self.client.get(manufacturer_url, {"name": "Unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            []
        )
