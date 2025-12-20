from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class PublicPagesTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivatePagesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)


class SearchTests(PrivatePagesTests):
    def setUp(self):
        super().setUp()

        self.driver1 = Driver.objects.create_user(
            username="john",
            password="pass",
            license_number="AAA11111"
        )
        self.driver2 = Driver.objects.create_user(
            username="mike",
            password="pass",
            license_number="BBB22222"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.car1 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer2
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )
        self.assertContains(response, "X5")
        self.assertNotContains(response, "A6")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")
