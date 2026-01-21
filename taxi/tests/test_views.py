from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_delete(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_update(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_update(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_manufacturer_delete(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
