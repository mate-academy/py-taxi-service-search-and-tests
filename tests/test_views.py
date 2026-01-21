from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA",
        )
        self.url = reverse("taxi:manufacturer-list")

    def test_manufacturer_list_view(self):
        self.client.login(
            username="testuser",
            password="password",
        )
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "Test Manufacturer"
        )

    def test_search_functionality(self):
        self.client.login(
            username="testuser",
            password="password",
        )
        response = self.client.get(
            self.url,
            {"name": "Test"}
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "Test Manufacturer"
        )


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA",
        )
        Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer,
        )
        self.url = reverse("taxi:car-list")

    def test_car_list_view(self):
        self.client.login(
            username="testuser",
            password="password",
        )
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertContains(
            response,
            "Test Car",
        )

    def test_car_search_functionality(self):
        self.client.login(
            username="testuser",
            password="password",
        )
        response = self.client.get(
            self.url,
            {"model": "Test"}
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "Test Car"
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )
        Driver.objects.create_user(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
            license_number="ABC11234",
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

    def test_driver_list_view(self):
        self.client.login(username="test", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")

    def test_driver_search_functionality(self):
        self.client.login(username="test", password="password")
        response = self.client.get(self.url, {"username": "testdriver"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.url = reverse("taxi:manufacturer-create")

    def test_create_manufacturer(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.url,
            {"name": "New Manufacturer", "country": "Germany"}
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(
            Manufacturer.objects.filter(name="New Manufacturer").exists()
        )


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        self.url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id]
        )

    def test_delete_manufacturer(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        self.url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id]
        )

    def test_update_manufacturer(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.url,
            {"name": "Updated Manufacturer", "country": "Germany"}
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Manufacturer")
