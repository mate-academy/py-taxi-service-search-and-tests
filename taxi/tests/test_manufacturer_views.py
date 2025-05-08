from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_VIEW_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_VIEW_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

    def test_manufacturer_list_view_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_view_login_required(self):
        response = self.client.get(MANUFACTURER_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_view_login_required(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_view_login_required(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="First Manufacturer",
            country="Test Country"
        )
        Manufacturer.objects.create(
            name="Second Manufacturer",
            country="Test Country1"
        )
        Manufacturer.objects.create(
            name="Third Manufacturer",
            country="Test Country2"
        )

    def test_manufacturer_list_view_without_search(self):
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertContains(response, "First Manufacturer")
        self.assertContains(response, "Second Manufacturer")
        self.assertContains(response, "Third Manufacturer")

    def test_manufacturer_list_view_with_search(self):
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL, {"name": "fir"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertContains(response, "First Manufacturer")
        self.assertNotContains(response, "Second Manufacturer")
        self.assertNotContains(response, "Third Manufacturer")

    def test_manufacturer_create_view(self):
        manufacturer_data = {
            "name": "Test manufacturer",
            "country": "Test country"
        }
        response_get = self.client.get(MANUFACTURER_CREATE_VIEW_URL)
        self.client.post(MANUFACTURER_CREATE_VIEW_URL, data=manufacturer_data)
        new_manufacturer = Manufacturer.objects.get(
            name=manufacturer_data["name"]
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/manufacturer_form.html")
        self.assertEqual(new_manufacturer.name, manufacturer_data["name"])
        self.assertEqual(
            new_manufacturer.country,
            manufacturer_data["country"]
        )

    def test_manufacturer_update_view(self):
        manufacturer_update_data = {
            "name": "Updated name",
            "country": "Updated country"
        }
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response_get = self.client.get(url)
        self.client.post(url, data=manufacturer_update_data)
        updated_manufacturer = Manufacturer.objects.get(
            id=self.manufacturer.id
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/manufacturer_form.html")
        self.assertEqual(
            updated_manufacturer.name,
            manufacturer_update_data["name"]
        )
        self.assertEqual(
            updated_manufacturer.country,
            manufacturer_update_data["country"]
        )

    def test_manufacturer_delete_view(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response_get = self.client.get(url)
        self.client.post(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(
            response_get,
            "taxi/manufacturer_confirm_delete.html"
        )
        self.assertEqual(Manufacturer.objects.count(), 2)
