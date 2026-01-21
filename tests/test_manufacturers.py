from django.urls import reverse
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Manufacturer.objects.create(
            name="Manufacturer1",
            country="Country1"
        )
        Manufacturer.objects.create(
            name="Manufacturer2",
            country="Country2"
        )
        Manufacturer.objects.create(
            name="Manufacturer3",
            country="Country3"
        )

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Manufacturer1"
        )
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")

    def test_search_empty(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=NonExistentCar"
        )
        self.assertContains(
            response, "There are no manufacturers in the service."
        )
