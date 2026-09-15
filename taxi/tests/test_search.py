from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="testpass123",
            license_number="ADM12345"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(toyota, response.context["manufacturer_list"])
        self.assertNotIn(bmw, response.context["manufacturer_list"])

    def test_search_manufacturer_is_case_insensitive(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "TOY"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(toyota, response.context["manufacturer_list"])
        self.assertNotIn(bmw, response.context["manufacturer_list"])

    def test_empty_manufacturer_search_returns_all_manufacturers(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(toyota, response.context["manufacturer_list"])
        self.assertIn(bmw, response.context["manufacturer_list"])

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        camry = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        corolla = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cam"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(camry, response.context["car_list"])
        self.assertNotIn(corolla, response.context["car_list"])

    def test_search_car_is_case_insensitive(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        x5 = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        m3 = Car.objects.create(
            model="M3",
            manufacturer=manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "x5"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(x5, response.context["car_list"])
        self.assertNotIn(m3, response.context["car_list"])

    def test_empty_car_search_returns_all_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        camry = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        corolla = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(camry, response.context["car_list"])
        self.assertIn(corolla, response.context["car_list"])

    def test_search_driver_by_username(self):
        john = Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            license_number="JOH12345"
        )
        alice = Driver.objects.create_user(
            username="alice_driver",
            password="testpass123",
            license_number="ALI12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(john, response.context["driver_list"])
        self.assertNotIn(alice, response.context["driver_list"])

    def test_search_driver_is_case_insensitive(self):
        john = Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            license_number="JOH12345"
        )
        alice = Driver.objects.create_user(
            username="alice_driver",
            password="testpass123",
            license_number="ALI12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(john, response.context["driver_list"])
        self.assertNotIn(alice, response.context["driver_list"])

    def test_empty_driver_search_returns_all_drivers(self):
        john = Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            license_number="JOH12345"
        )
        alice = Driver.objects.create_user(
            username="alice_driver",
            password="testpass123",
            license_number="ALI12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(john, response.context["driver_list"])
        self.assertIn(alice, response.context["driver_list"])
