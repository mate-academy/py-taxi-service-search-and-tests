from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PublicViewsTests(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_accessible(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_accessible(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_accessible(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)


class PrivateSearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Test"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "coro"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")

    def test_driver_search(self):
        other = Driver.objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="XYZ98765",
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(other, response.context["driver_list"])
        self.assertNotIn(self.user, response.context["driver_list"])
