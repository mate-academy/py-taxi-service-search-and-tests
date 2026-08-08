from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="alex",
            password="test12345",
            license_number="XYZ54321",
        )

        manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer1,
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer2,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "jo"},
        )

        self.assertContains(response, "john")
        self.assertNotContains(response, "alex")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "X5"},
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "Model S")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "BMW"},
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Tesla")
