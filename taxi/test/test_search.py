from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.login(username="test", password="test123")

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_search_contains(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "Tesla"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_icontains(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "tes"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_with_out_arguments(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Ford")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="pass123"
        )
        self.client.login(username="testuser", password="pass123")

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X5", manufacturer=self.manufacturer)
        Car.objects.create(model="X3", manufacturer=self.manufacturer)
        Car.objects.create(
            model="Model S",
            manufacturer=Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            )
        )

    def test_search_exact_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "X5"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_search_partial_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "X"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertContains(response, "X3")

    def test_search_empty_query(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertContains(response, "X3")
        self.assertContains(response, "Model S")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="admin123"
        )
        self.client.login(username="admin", password="admin123")

        Driver.objects.create(
            username="text",
            password="text",
            license_number="ABC1234",
            first_name="Imya",
            last_name="Familia"
        )
        Driver.objects.create(
            username="test", password="test", license_number="XYZ7890",
            first_name="Imya", last_name="Familia"
        )
        Driver.objects.create(
            username="shozadriver",
            password="shozadriver",
            license_number="LMN4567",
            first_name="Imya",
            last_name="Familia"
        )

    def test_search_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "text"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text")

    def test_search_by_partial_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_search_empty_query(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text")
        self.assertContains(response, "test")
        self.assertContains(response, "shozadriver")
