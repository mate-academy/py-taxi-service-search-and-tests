from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertRedirects(
            res,
            f"{settings.LOGIN_URL}?next={MANUFACTURER_LIST_URL}"
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_123",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_retrieve_manufacturer(self):

        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturer)
        )

    def test_list_view_displays_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )
        self.assertIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )

    def test_search_filters_queryset(self):
        """
        Search form should filter manufacturers by name.
        """
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )
        manufacturer_list = response.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturer_list)
        self.assertNotIn(self.manufacturer2, manufacturer_list)

    def test_create_manufacturer(self):
        """
        Should successfully create a new manufacturer.
        """
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "BMW", "country": "Germany"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Manufacturer.objects.filter(name="BMW").exists())

    def test_update_manufacturer(self):
        """
        Should successfully update a manufacturer.
        """
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer1.id])
        response = self.client.post(
            url, {"name": "Toyota Updated", "country": "Japan"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.manufacturer1.refresh_from_db()
        self.assertEqual(self.manufacturer1.name, "Toyota Updated")

    def test_delete_manufacturer(self):
        """
        Should successfully delete a manufacturer.
        """
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer2.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer2.id).exists()
        )

    def test_search_no_results_returns_empty_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "xyz"})
        self.assertFalse(response.context["manufacturer_list"].exists())

    def test_search_empty_query_returns_full_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        manufacturer_list = response.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturer_list)
        self.assertIn(self.manufacturer2, manufacturer_list)
