from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewsTest(TestCase):
    def test_login_required_for_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Manufacturer.objects.create(name="Ford", country="USA")

        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        Car.objects.create(model="Focus", manufacturer=self.manufacturer)

        get_user_model().objects.create_user(
            username="another_driver",
            password="testpass123",
            license_number="XYZ98765",
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Focus")

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test_user"}
        )
        self.assertContains(response, "test_user")
        self.assertNotContains(response, "another_driver")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "Camry")
        self.assertContains(response, "Focus")
