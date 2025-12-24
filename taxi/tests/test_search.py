from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password")
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA")
        self.manufacturer3 = Manufacturer.objects.create(
            name="Tesla", country="USA")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Ford"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Tesla")


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword")
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer)

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="john.doe",
            first_name="John",
            last_name="Doe",
            license_number="AAA12345"
        )
        self.driver2 = Driver.objects.create(
            username="jane.smith",
            first_name="Jane",
            last_name="Smith",
            license_number="BBB12345"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john.doe")
        self.assertNotContains(response, "jane.smith")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john.doe")
        self.assertContains(response, "jane.smith")
