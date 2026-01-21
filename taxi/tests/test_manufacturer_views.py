from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Honda")
        Manufacturer.objects.create(name="Ford")
        self.client.login(username="testuser", password="testpass")

    def test_manufacturers_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_lists_all_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
            + "?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_manufacturers_search_functionality(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
            + "?name=Toyota"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Toyota"
        )

    def test_manufacturers_invalid_search_form(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
            + "?name="
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_get_queryset_with_manufacturer_name(self):
        response = self.client.get("/manufacturers/?name=Toyota")
        queryset = response.context["manufacturer_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].name, "Toyota")

    def test_manufacturers_search_case_insensitive(self):
        response = self.client.get("/manufacturers/?name=FORD")
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
