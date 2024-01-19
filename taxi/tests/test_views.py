from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1",
        )
        self.client.force_login(self.user)

    def test_required_manufacturers(self):
        Manufacturer.objects.create(name="fff")
        Manufacturer.objects.create(name="ccc")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturers,
        )
