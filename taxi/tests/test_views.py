from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="alex_driver",
            password="pass123",
            license_number="ABC122"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="john_driver",
            password="pass123",
            license_number="ABC123"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "alex"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="A6", manufacturer=manufacturer)

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertNotContains(response, "A6")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Audi")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "bm"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")
