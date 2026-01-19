from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="TestUser",
            password="password",
            license_number="123456",
        )
        self.user2 = get_user_model().objects.create_user(
            username="NotFound",
            password="password",
            license_number="1234567",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="NotFound",
            country="TestCountry",
        )
        self.car1 = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="NotFound",
            manufacturer=self.manufacturer1,
        )
        self.client = Client()
        self.client.force_login(self.user1)

    def test_car_search(self):
        data = {
            "model": self.car1.model,
        }
        url = reverse("taxi:car-list")
        res = self.client.get(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car1.model)
        self.assertNotContains(res, self.car2.model)

    def test_manufacturer_search(self):
        data = {
            "name": self.manufacturer1.name,
        }
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.manufacturer1.name)
        self.assertNotContains(res, self.manufacturer2.name)

    def test_driver_search(self):
        data = {
            "username": self.user1.username,
        }
        url = reverse("taxi:driver-list")
        res = self.client.get(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user1.username)
        self.assertNotContains(res, self.user2.username)
