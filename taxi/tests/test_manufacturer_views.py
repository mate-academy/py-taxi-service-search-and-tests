from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required_list_page(self):
        resp = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="LIC12345",
        )
        self.client.force_login(self.user)

    def test_get_manufacturer_list_page(self):
        Manufacturer.objects.create(
            name="First manufacturer",
            country="UK"
        )
        Manufacturer.objects.create(
            name="Second manufacturer",
            country="US"
        )

        resp = self.client.get(MANUFACTURERS_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers),
        )
