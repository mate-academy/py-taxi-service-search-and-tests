from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer, Driver


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.car1 = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.car2 = Car.objects.create(model="M3", manufacturer=manufacturer)
        self.car3 = Car.objects.create(model="i8", manufacturer=manufacturer)

    def test_car_list_view_returns_all_cars(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

    def test_car_list_view_search_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "M3"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car3.model)


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.login(username="testuser", password="testpass123")

        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="pass12345",
            license_number="DRV00001",
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="pass12345",
            license_number="DRV00002",
        )

    def test_driver_list_view_returns_all_drivers(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)

    def test_driver_list_view_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "driver1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

    def test_manufacturer_list_view_returns_all_manufacturers(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)

    def test_manufacturer_list_view_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BMW"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
