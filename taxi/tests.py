from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTaxiTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_works(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL, {"name": "Toy"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")

    def test_car_list_works(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(CAR_URL, {"model": "Cor"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")

    def test_driver_list_works(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="jane_smith",
            password="password123",
            license_number="XYZ67890"
        )

        response = self.client.get(DRIVER_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
