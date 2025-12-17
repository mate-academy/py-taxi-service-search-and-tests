from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer

User = get_user_model()


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="ABC12345",
        )
        self.user2 = User.objects.create_user(
            username="bob",
            password="test12345",
            license_number="DEF67890",
        )

        self.client.login(username="alex_driver", password="test12345")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"q": "alex"},
        )

        self.assertContains(response, "alex_driver")
        self.assertNotContains(response, "bob")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="driver",
            password="test12345",
            license_number="GHI11111",
        )
        self.client.login(username="driver", password="test12345")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"q": "Corolla"},
        )

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="driver",
            password="test12345",
            license_number="JKL22222",
        )
        self.client.login(username="driver", password="test12345")

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "BMW"},
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")
