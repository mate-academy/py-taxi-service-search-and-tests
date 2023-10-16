from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class SearchTestCase(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BingChilling",
            country="China"
        )
        self.car = Car.objects.create(
            model="test_model_car",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="riceman",
            password="ChinaIsTheBest",
            first_name="BimBim",
            last_name="BamBam",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_car_search(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "test_model_car"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "test_model_car"
        )

    def test_driver_search(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "riceman"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "riceman")

    def test_manufacturer_search(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "BingChilling"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BingChilling")
