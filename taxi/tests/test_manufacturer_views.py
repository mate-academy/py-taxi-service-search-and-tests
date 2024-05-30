from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer

manufacturer_url = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.url = manufacturer_url

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.force_login(self.user)
        self.url = manufacturer_url

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_retrieve_manufacturers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all().order_by("name")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_context_contains_correct_data(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context["manufacturer_list"])
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.all().order_by("name"),
            transform=lambda x: x,
        )

    def test_page_contains_manufacturer_names(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
