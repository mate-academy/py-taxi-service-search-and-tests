from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_context_data(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["name"], "Toyota")

    def test_get_queryset_with_search(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        manufacturers = Manufacturer.objects.filter(name__icontains="Toyota")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
