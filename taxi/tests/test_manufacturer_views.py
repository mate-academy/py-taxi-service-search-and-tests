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
            username="Test",
            password="Test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1", country="TestCountry1")
        Manufacturer.objects.create(name="Test2", country="TestCountry2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_filters_queryset(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Test1"})

        self.assertEqual(response.status_code, 200)

        expected = Manufacturer.objects.filter(name__icontains="Test1")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(expected)
        )

    def test_search_empty_returns_all(self):
        response = self.client.get(MANUFACTURER_URL, {"name": ""})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )

    def test_create_manufacturer(self):
        form_data = {
            "name": "TestName",
            "country": "TestCountry"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):

        form_data = {
            "name": "NewName",
            "country": "NewCountry"
        }
        self.client.post(reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id]
        ), data=form_data)
        self.manufacturer.refresh_from_db()

        self.assertEqual(self.manufacturer.name, form_data["name"])
        self.assertEqual(self.manufacturer.country, form_data["country"])

    def test_confirm_delete_manufacturer(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-delete",
                args=[self.manufacturer.id]
            ), follow=True
        )
        self.assertContains(response, "Delete manufacturer?")

    def test_delete_manufacturer(self):
        post_response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                args=[self.manufacturer.id]
            ), follow=True
        )
        self.assertRedirects(post_response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(
                id=self.manufacturer.id).exists()
        )
