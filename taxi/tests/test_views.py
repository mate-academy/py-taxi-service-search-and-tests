from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturer(TestCase):
    def test_login(self):
        res = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )

        self.client.force_login(self.user)

    def test_retrieve(self):
        Manufacturer.objects.create(
            name="test",
            country="test2"
        )
        manufacturer = Manufacturer.objects.all()
        res = self.client.get(MANUFACTURERS_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )
