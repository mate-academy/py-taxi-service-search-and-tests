from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="dispatcher",
            password="testpass123",
            license_number="DDD12345",
        )
        self.client.force_login(self.user)

    def test_driver_search_filters_by_username(self):
        Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            license_number="EEE12345",
        )
        Driver.objects.create_user(
            username="jane_driver",
            password="testpass123",
            license_number="FFF12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "jane_driver")

    def test_car_search_filters_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        Car.objects.create(model="Civic", manufacturer=manufacturer)
        Car.objects.create(model="Accord", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "civ"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "Accord")

    def test_manufacturer_search_filters_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_query_is_preserved_in_pagination(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany",
        )
        for number in range(6):
            Car.objects.create(
                model=f"Golf {number}",
                manufacturer=manufacturer,
            )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "Golf"},
        )

        self.assertContains(response, "search=Golf&page=2")
