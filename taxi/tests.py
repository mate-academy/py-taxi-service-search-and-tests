from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.test_manuf = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.test_driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            password="password123",
            licence_number="YTG34567",
        )
        self.test_car = Car.objects.create(
            model="test model",
            manufacturer=self.test_manuf
        )
        self.test_car.drivers.set([self.test_driver])

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.test_manuf),
            f"{self.test_manuf.name} {self.test_manuf.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.test_driver),
            f"{self.test_driver.username} ({self.test_driver.first_name} "
            f"{self.test_driver.last_name})",
        )

    def test_car_str(self):
        self.assertEqual(str(self.test_car), self.test_car.model)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.manuf1 = Manufacturer.objects.create(
            name="Test Manufacturer", country="US"
        )
        self.manuf2 = Manufacturer.objects.create(
            name="BMW Motors", country="Germany"
        )

        # створюємо користувача, бо сторінка під LoginRequiredMixin
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_returns_correct_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BMW"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW Motors")
        self.assertNotContains(response, "Test Manufacturer")

    def test_search_is_case_insensitive(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "bmw"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW Motors")

    def test_search_with_no_query_returns_all(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW Motors")
        self.assertContains(response, "Test Manufacturer")


class CarSearchTest(TestCase):
    def setUp(self):
        self.manuf1 = Manufacturer.objects.create(
            name="Tesla", country="US"
        )
        self.test_driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            password="password123",
            license_number="LIJ23456",
        )
        self.test_car = Car.objects.create(
            model="S1",
            manufacturer=self.manuf1,
        )
        self.test_car.drivers.set([self.test_driver])

        # створюємо користувача, бо сторінка під LoginRequiredMixin
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_returns_correct_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "S1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "S1")

    def test_search_is_case_insensitive(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "S1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_with_no_query_returns_all(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertContains(response, "S1")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.test_driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            password="password123",
            license_number="ERW12345",
        )

        # створюємо користувача, бо сторінка під LoginRequiredMixin
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_returns_correct_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test_driver"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")
        self.assertNotContains(response, "Test Driver")

    def test_search_is_case_insensitive(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test_driver"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")

    def test_search_with_no_query_returns_all(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")
        self.assertContains(response, "Test Driver")
