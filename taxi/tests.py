from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertContains(response, "testuser")

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=wrong"
        )

        self.assertContains(
            response,
            "There are no drivers in the service."
        )

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Camry"
        )
        self.assertContains(response, "Camry")

        response = self.client.get(
            reverse("taxi:car-list") + "?model=wrong"
        )
        self.assertNotContains(
            response,
            "<td>Camry</td>",
            html=True
        )

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertContains(response, "Toyota")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=wrong"
        )
        self.assertNotContains(
            response,
            "<td>Toyota</td>",
            html=True
        )
