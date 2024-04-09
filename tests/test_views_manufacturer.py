from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicFormatTest(TestCase):

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Test Manufacturer",
            "country": "Test Country",
        }
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data
        )
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])
        self.assertRedirects(response, "/manufacturers/")

    def test_query_search_filter_by_part_of_model(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Test Country1",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country2",
        )
        response = self.client.get("/manufacturers/", {"name": "facturer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            [manufacturer1, manufacturer2]
        )

    def test_search_with_empty_query(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            Manufacturer.objects.count()
        )

    def test_search_with_invalid_data(self):
        response = self.client.get("/manufacturers/", {"name": "model"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
