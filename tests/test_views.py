from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_manufacturers(self) -> None:
        Manufacturer.objects.create(name="Toyota")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
