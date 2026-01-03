from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.forms import ManufacturerSearchForm

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewsTests(TestCase):
    def test_access_not_logged_in_users(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_name1", country="test_country1"
        )

    def test_manufacturer_list_view(self):
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(
            res, "taxi/manufacturer_list.html"
        )
        self.assertIsInstance(
            res.context["search_manufacturer"], ManufacturerSearchForm
        )

    def test_manufacturer_search(self):
        url = f"{MANUFACTURER_URL}?name=test_name1"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 1)
        self.assertEqual(
            res.context["manufacturer_list"][0], self.manufacturer
        )

    def test_manufacturer_create_view_get(self):
        url = reverse("taxi:manufacturer-create")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "taxi/manufacturer_form.html"
        )

    def test_manufacturer_create_view_post(self):
        url = reverse("taxi:manufacturer-create")
        data = {
            "name": "New Manufacturer",
            "country": "New Country"
        }
        res = self.client.post(url, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="New Manufacturer").exists()
        )

    def test_manufacturer_update_view_get(self):
        url = reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "taxi/manufacturer_form.html"
        )

    def test_manufacturer_update_view_post(self):
        url = reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]
        )
        data = {
            "name": "Updated Manufacturer",
            "country": "Updated Country"
        }
        res = self.client.post(url, data=data)

        self.assertEqual(res.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Manufacturer")
        self.assertEqual(self.manufacturer.country, "Updated Country")

    def test_manufacturer_delete_view_get(self):
        url = reverse(
            "taxi:manufacturer-delete", args=[self.manufacturer.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "taxi/manufacturer_confirm_delete.html"
        )

    def test_manufacturer_delete_view_post(self):
        url = reverse(
            "taxi:manufacturer-delete", args=[self.manufacturer.id]
        )
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
