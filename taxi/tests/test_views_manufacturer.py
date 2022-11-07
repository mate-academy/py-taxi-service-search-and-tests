from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Lincoln", country="USA")
        Manufacturer.objects.create(name="Suzuki", country="Japan")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(len(response.context["manufacturer_list"]), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
