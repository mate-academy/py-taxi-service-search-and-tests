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
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test1_name",
            country="test1_country"
        )

    def test_retrieve_manufacturer(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_search_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL + "?name=1")
        manufacturer = Manufacturer.objects.filter(name__icontains="1")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "new_manufacturer", "country": "new_country"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="new_manufacturer").exists()
        )

    def test_update_manufacturer(self):
        res = self.client.post(
            reverse("taxi:manufacturer-update", args=[1]),
            {"name": "updated_name", "country": "updated_country"}
        )
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))
        self.assertTrue(
            Manufacturer.objects.filter(name="updated_name").exists()
        )

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                args=[1]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=1).exists()
        )
