from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

INDEX_URL = reverse("taxi:index")


class PublicIndexTests(TestCase):
    def test_login_required(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_login_required_(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_index_view_status_code(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)


class PublicManufacturerListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")

    def test_login_required_(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        get_user_model().objects.create_user(
            username="test_user",
            password="12345"
        )
        Manufacturer.objects.create(name="Manufacturer1")
        Manufacturer.objects.create(name="Manufacturer2")

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(username="test_user")
        self.client.login(username="test_user", password="12345")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Manufacturer1"}
        )
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["name"], "Manufacturer1"
        )

    def test_search_filter(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Manufacturer1"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Manufacturer1"
        )
