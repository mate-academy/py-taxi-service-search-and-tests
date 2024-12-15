# flake8: noqa: E731

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = lambda pk: reverse(
    "taxi:manufacturer-update", args=[pk]
)
MANUFACTURER_DELETE_URL = lambda pk: reverse(
    "taxi:manufacturer-delete", args=[pk]
)


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1223",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )

    def test_search_manufacturer_by_username(self):
        """Test searching manufacturer by name"""
        Manufacturer.objects.create(
            name="New Manufacturer",
            country="US",
        )
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": "Test Manufacturer"}
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            1
        )
        self.assertEqual(
            response.context["manufacturer_list"][0],
            self.manufacturer
        )

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Test Manufacturer 1", country="US")
        Manufacturer.objects.create(name="Test Manufacturer 2", country="US")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(len(manufacturers), 3)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_create_manufacturer(self):
        from_data = {
            "name": "New Manufacturer",
            "country": "US",
        }
        response = self.client.post(MANUFACTURER_CREATE_URL, from_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="New Manufacturer").exists()
        )

    def test_update_manufacturer(self):
        update_url = MANUFACTURER_UPDATE_URL(self.manufacturer.id)
        form_data = {
            "name": "Updated Manufacturer",
            "country": "Germany",
        }
        response = self.client.post(update_url, data=form_data)
        self.manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(self.manufacturer.name, "Updated Manufacturer")
        self.assertEqual(self.manufacturer.country, "Germany")

    def test_delete_manufacturer(self):
        delete_url = MANUFACTURER_DELETE_URL(self.manufacturer.id)
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
