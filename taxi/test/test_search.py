from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


class DriverSearchTests(TestCase):
    def setUp(self):

        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="driver1",
            first_name="first test",
            last_name="last test",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            first_name="first test",
            last_name="last test",
            license_number="XYZ67890"
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse(
                "taxi:driver-list"), {"username": "driver1"}
        )
        self.assertContains(
            response,
            self.driver1.username
        )
        self.assertNotContains(
            response,
            self.driver2.username
        )


class CarSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertContains(
            response,
            self.car1.model
        )


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertContains(
            response, self.manufacturer1.name
        )
        self.assertNotContains(
            response, self.manufacturer2.name
        )
