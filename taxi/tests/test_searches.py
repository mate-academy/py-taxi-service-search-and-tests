from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarSearchTest(TestCase):
    def setUp(self):
        self.driver_logged = get_user_model().objects.create_user(
            username="Logged User",
            password="Test Password",
            license_number="AAA00000",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.driver = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
            license_number="ABC12345",
        )
        self.car1 = Car.objects.create(
            model="Test Model1",
            manufacturer=self.manufacturer,
        )
        self.car1.drivers.add(self.driver)

        self.car2 = Car.objects.create(
            model="Test Model2",
            manufacturer=self.manufacturer,
        )
        self.car2.drivers.add(self.driver)
        self.client.force_login(self.driver_logged)

    def test_search_by_exact_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": self.car1.model}
        )
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertEqual(response.status_code, 200)

    def test_search_by_part_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Test"}
        )
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertEqual(response.status_code, 200)

    def test_search_no_match(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Other"}
        )
        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertEqual(response.status_code, 200)

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""}
        )
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertEqual(response.status_code, 200)


class DriverSearchTest(TestCase):
    def setUp(self):
        self.driver_logged = get_user_model().objects.create_user(
            username="Logged User",
            password="Test Password",
            license_number="AAA00000",
        )
        self.driver1 = get_user_model().objects.create_user(
            username="Test User1",
            password="Test Password",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="Test User2",
            password="Test Password",
            license_number="DEF67890",
        )
        self.client.force_login(self.driver_logged)

    def test_search_by_exact_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": self.driver1.username}
        )
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertEqual(response.status_code, 200)

    def test_search_by_part_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "Test"}
        )
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertEqual(response.status_code, 200)

    def test_search_no_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "Other"}
        )
        self.assertNotContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertEqual(response.status_code, 200)

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""}
        )
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertEqual(response.status_code, 200)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.driver_logged = get_user_model().objects.create_user(
            username="Logged User",
            password="Test Password",
            license_number="AAA00000",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Test Country",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country",
        )

        self.client.force_login(self.driver_logged)

    def test_search_by_exact_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": self.manufacturer1.name}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertEqual(response.status_code, 200)

    def test_search_by_part_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertEqual(response.status_code, 200)

    def test_search_no_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Other"}
        )
        self.assertNotContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertEqual(response.status_code, 200)

    def test_search_empty_query(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertEqual(response.status_code, 200)
