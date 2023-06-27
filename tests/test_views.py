from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(name="name")
        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["manufacturer_list"]),
            set(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
