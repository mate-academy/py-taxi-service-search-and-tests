from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[1])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[1])


class PublicManufacturerTests(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "TestUser",
            "TestPassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed("taxi/manufacturer_list.html")
