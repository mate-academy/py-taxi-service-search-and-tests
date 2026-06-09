from django.contrib.auth import get_user_model
from django.template.defaultfilters import cut
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_search_cars_by_model(self):
        honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        Car.objects.create(
            manufacturer=honda,
            model="Honda Civic",
        )

        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(
            manufacturer=toyota,
            model="Toyota Corolla",
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            data={"car_model": "Corolla"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Corolla")
        self.assertNotContains(response, "Honda Civic")

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="another_user",
            password="password",
            license_number="DEF12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test_user"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_user")
        self.assertNotContains(response, "another_user")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country",
        )
        Manufacturer.objects.create(
            name="Another Manufacturer",
            country="Another country",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"manufacturer_name": "Test"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertNotContains(response, "Another Manufacturer")
