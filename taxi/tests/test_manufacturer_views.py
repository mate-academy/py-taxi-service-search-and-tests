from django.contrib.auth import get_user_model

from taxi.models import Manufacturer
from django.test import TestCase, Client
from django.urls import reverse

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="TestPassword1",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers_status_code(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
