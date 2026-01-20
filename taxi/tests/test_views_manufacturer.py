from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTest(TestCase):
    def test_login_list_required(self):
        result_list = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(result_list.status_code, 200)

    def test_login_create_required(self):
        result_create = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEqual(result_create.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "test_name_username",
            "test_password"
        )
        self.client.force_login(self.driver)

    def test_login_create_required(self):
        Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html")

    def test_login_update_required(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        url = reverse("taxi:manufacturer-update", args=[manufacturer.pk])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_login_delete_required(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
