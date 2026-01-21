from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        username = "tester"
        password = "password123"

        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.client.login(username=username, password=password)

        self.driver1 = get_user_model().objects.create_user(
            username="mike",
            password="test123",
            first_name="Mike",
            last_name="Smith",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="john",
            password="test123",
            first_name="John",
            last_name="Doe",
            license_number="XYZ67890"
        )

        self.audi = Manufacturer.objects.create(name="Audi", country="Germany")
        self.bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        Car.objects.create(model="A6", manufacturer=self.audi)
        Car.objects.create(model="Q5", manufacturer=self.audi)
        Car.objects.create(model="X5", manufacturer=self.bmw)

    def test_search_by_driver(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "mike"})
        self.assertContains(response, "mike")
        self.assertNotContains(response, "john")

    def test_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "A6"})
        self.assertContains(response, "A6")
        self.assertNotContains(response, "Q5")
        self.assertNotContains(response, "X5")

    def test_search_by_manufacturer(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "BMW"})
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")
