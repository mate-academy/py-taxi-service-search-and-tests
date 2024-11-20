from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password123",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="test_password1",
            license_number="123456",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="jane_smith",
            password="test_password2",
            license_number="654321",
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer2,
        )
        self.car1.drivers.add(self.driver1, self.driver2)
        self.car2.drivers.add(self.driver2, self.driver1)

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"},
        )
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Corolla"},
        )
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_search_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Toyota"},
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
