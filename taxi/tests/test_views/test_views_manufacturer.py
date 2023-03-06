from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_list_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_create_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="1234qwer"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_create_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertEqual(res.status_code, 200)
