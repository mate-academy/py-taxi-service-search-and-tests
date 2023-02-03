from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_get_manufacturer(self):
        Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="Ferrary", country="China")
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
