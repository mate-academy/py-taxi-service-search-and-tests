from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.car_1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

        self.car_2 = Car.objects.create(
            model="Yaris",
            manufacturer=self.manufacturer,
        )

    def test_car_list_without_filter(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Yaris")

    def test_car_list_filter_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "corol"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Yaris")


class ManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.manufacturer_2 = Manufacturer.objects.create(
            name="Ford",
            country="United States",
        )

    def test_manufacturer_list_without_filter(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_manufacturer_list_filter_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "toy"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")


class DriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        self.user_1 = get_user_model().objects.create_user(
            username="Eduardo",
            password="test1234",
            license_number="TTT12345",
        )

        self.user_2 = get_user_model().objects.create_user(
            username="Rodrigo",
            password="test1234",
            license_number="YUH65454"
        )

    def test_driver_list_without_filter(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eduardo")
        self.assertContains(response, "Rodrigo")

    def test_driver_list_filter_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "Edu"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eduardo")
        self.assertNotContains(response, "Rodrigo")
