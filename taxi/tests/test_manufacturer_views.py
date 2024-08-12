from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testtest123",
        )
        self.client.force_login(self.user)

    def test_authorised_user_can_access(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_manufacturer(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Spain",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Germany",
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        queryset = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(queryset)
        )
        self.assertContains(response, manufacturer1.name)
        self.assertContains(response, manufacturer2.name)
