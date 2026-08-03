from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchResultsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            password="pbkdf2_sha256$320000$6uM28XWOFX6ewyloJzj"
                     "qmt$L+ZhofPylneoaL2iZS4sZu4ZMUNb4oIevfAdzOMn/eE=",
            username="admin.user",
            first_name="Admin",
            last_name="User",
            license_number="ADM56984",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="AUDI",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        get_user_model().objects.create_user(
            username="john",
            password="test12345",
            license_number="DEF12345",
        )
        get_user_model().objects.create_user(
            username="mike",
            password="test12345",
            license_number="GHI12345",
        )
        Car.objects.create(
            model="A4",
            manufacturer_id=1,
        )
        Car.objects.create(
            model="M5",
            manufacturer_id=2,
        )

    def test_drivers_search_gives_correct_result(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")

    def test_cars_search_gives_correct_result(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "A4"},
        )

        self.assertContains(response, "A4")
        self.assertNotContains(response, "M5")

    def test_manufacturers_search_gives_correct_result(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "AUDI"},
        )

        self.assertContains(response, "AUDI")
        self.assertNotContains(response, "BMW")
