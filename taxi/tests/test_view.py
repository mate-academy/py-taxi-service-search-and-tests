from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class PublicTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_drivers(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cars(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser1", password="testpass1", license_number="1234567"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="country1")
        Manufacturer.objects.create(name="test2", country="country2")
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
