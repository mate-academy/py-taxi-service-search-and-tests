from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car

User = get_user_model()


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="BMW", country="Germany")
        self.m3 = Manufacturer.objects.create(name="Ford", country="USA")

    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_search_by_name(self):
        self.client.login(username="testuser", password="test12345")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Ford")

    def test_search_case_insensitive(self):
        self.client.login(username="testuser", password="test12345")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )

        self.assertContains(response, "Toyota")

    def test_search_empty_query_returns_all(self):
        self.client.login(username="testuser", password="test12345")

        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            3
        )


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="test12345"
        )

        self.d1 = Driver.objects.create_user(
            username="john_doe",
            password="123",
            license_number="AAA11111"
        )
        self.d2 = Driver.objects.create_user(
            username="mary_smith",
            password="123",
            license_number="BBB22222"
        )

    def test_search_driver_by_username(self):
        self.client.login(username="admin", password="test12345")

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "mary_smith")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.c1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.c2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        self.client.login(username="testuser", password="test12345")

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"}
        )

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")


    class ManufacturerSearchTests(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username="testuser",
                password="test12345"
            )

            self.client.login(
                username="testuser",
                password="test12345"
            )

            Manufacturer.objects.create(name="Toyota", country="Japan")
            Manufacturer.objects.create(name="BMW", country="Germany")
            Manufacturer.objects.create(name="Ford", country="USA")

        def test_search_by_name(self):
            response = self.client.get(
                reverse("taxi:manufacturer-list"),
                {"name": "Toy"}
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Toyota")
            self.assertNotContains(response, "BMW")

        def test_search_case_insensitive(self):
            response = self.client.get(
                reverse("taxi:manufacturer-list"),
                {"name": "toy"}
            )

            self.assertContains(response, "Toyota")

        def test_search_empty_query_returns_all(self):
            response = self.client.get(
                reverse("taxi:manufacturer-list")
            )

            self.assertEqual(
                len(response.context["manufacturer_list"]),
                3)
