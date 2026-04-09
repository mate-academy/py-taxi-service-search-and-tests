from http.client import responses

from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class SearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="Dmytro_Milka",
            license_number="123456",
            first_name="Dmytro",
            last_name="Milko",
        )
        self.driver2 = Driver.objects.create(
            username="Oleg_Virto",
            license_number="000456",
            first_name="Oleh",
            last_name="Virto",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.car = Car.objects.create(
            model="M3",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver2)

        self.client.force_login(self.driver1)

    def test_driver_search_by_username(self):
        self.url = reverse("taxi:driver-list")
        response = self.client.get(self.url, {"username": "Dmytro"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dmytro_Milka")

    def test_manufacturer_search_by_name(self):
        self.url = reverse("taxi:manufacturer-list")
        response = self.client.get(self.url, {"name": self.manufacturer.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")

    def test_car_search_by_model(self):
        self.url = reverse("taxi:car-list")
        response = self.client.get(self.url, {"model": "M3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "M3")


class ModelTests(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create(
            license_number="123456",
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} "
                         f"{driver.last_name})")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} "
                         f"{manufacturer.country}")
