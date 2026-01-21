from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class ManufacturerListTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_correct_pagination(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_correct_search_form_present(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTrue("search_form" in response.context)
        self.assertTrue(
            isinstance(response.context["search_form"], ManufacturerSearchForm)
        )

    def test_search_form_correct_output(self):
        url = MANUFACTURER_LIST_URL + "?" + urlencode({"name": "g"})
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="g")),
        )


class ManufacturerCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_correct_redirect_after_manufacturer_create(self):
        response = self.client.post(
            MANUFACTURER_CREATE_URL,
            {"name": "test_name", "country": "test_country"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)


class ManufacturerUpdateTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_correct_redirect_after_manufacturer_update(self):
        response = self.client.post(
            MANUFACTURER_UPDATE_URL,
            {"name": "test_name", "country": "test_country"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)


class ManufacturerDeleteTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_manufacturer_deleted(self):
        response = self.client.post(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(pk=1).exists())

    def test_correct_redirect_after_manufacturer_delete(self):
        response = self.client.post(MANUFACTURER_DELETE_URL)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)


class LoginRequiredTests(TestCase):
    def test_manufacturer_list_restricted_to_logged_in(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_restricted_to_logged_in(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_restricted_to_logged_in(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_restricted_to_logged_in(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)
