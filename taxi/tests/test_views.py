from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicCarTests(TestCase):
    def test_login_required_for_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 302)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12345",
        )

        self.other_driver = get_user_model().objects.create_user(
            username="gabriel",
            password="testpassword",
            license_number="DEF12345",
        )

        self.client.force_login(self.driver)

        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota,
        )

        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=self.honda,
        )

    def test_toggle_assign_driver_to_car(self):
        url = reverse(
            "taxi:toggle-car-assign",
            args=[self.car1.id]
        )

        self.assertFalse(
            self.car1.drivers.filter(id=self.driver.id).exists()
        )

        response = self.client.get(url)

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car1.id])
        )

        self.assertTrue(
            self.car1.drivers.filter(id=self.driver.id).exists()
        )

        self.client.get(url)

        self.assertFalse(
            self.car1.drivers.filter(id=self.driver.id).exists()
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            CAR_LIST_URL,
            {"model": "Corolla"}
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]

        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_search_driver_by_username(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": "gabriel"}
        )

        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]

        self.assertIn(self.other_driver, drivers)
        self.assertNotIn(self.driver, drivers)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "Toyota"}
        )

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]

        self.assertIn(self.toyota, manufacturers)
        self.assertNotIn(self.honda, manufacturers)
