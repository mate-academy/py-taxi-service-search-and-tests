from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="ij5rdi",
            password="plo038bvysd"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Hyundai",
            country="South Korea"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Suzuki",
            country="Japan"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Ford"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Hyundai")
        self.assertNotContains(response, "Suzuki")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Suzuki")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Hyundai")


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="franki",
            password="x6c5v1b8ndsk")
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="German"
        )
        self.car1 = Car.objects.create(
            model="A7",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Q5",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "A7"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A7")
        self.assertNotContains(response, "Q5")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A7")
        self.assertContains(response, "Q5")


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="grick",
            password="aA5c6!908")
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="red_flag",
            first_name="Carl",
            last_name="White",
            license_number="XTA63383"
        )
        self.driver2 = Driver.objects.create(
            username="kubik_a",
            first_name="Sam",
            last_name="Folk",
            license_number="OLO28199"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "red_flag"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "red_flag")
        self.assertNotContains(response, "kubik_a")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "red_flag")
        self.assertContains(response, "kubik_a")
