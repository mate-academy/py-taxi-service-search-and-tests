from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = "taxi:manufacturer-update"
MANUFACTURER_DELETE_URL = "taxi:manufacturer-delete"
PAGINATION = 5

TestCase.fixtures = ["taxi_service_db_data.json", ]


class PublicManufacturerViewsTests(TestCase):

    def test_login_required_for_list_view(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_create_view(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_update_view(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.get(
            reverse(MANUFACTURER_UPDATE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_delete_view(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.post(
            reverse(MANUFACTURER_DELETE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_password_123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_response_with_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_is_paginated(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            PAGINATION
        )

    def test_manufacturer_list_search_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTrue("name" in response.context_data["search_form"].fields)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer_list = list(Manufacturer.objects.all()[:PAGINATION])
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturer_list
        )


class PrivateManufacturerCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_password_123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_create_response_with_correct_template(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_create_has_correct_success_url(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            MANUFACTURER_LIST_URL
        )

    def test_create_manufacturer(self):
        form_data = {
            "name": "test_name",
            "country": "test_country",
        }
        response = self.client.post(MANUFACTURER_CREATE_URL, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.last().name, form_data["name"])
        self.assertEqual(
            Manufacturer.objects.last().country,
            form_data["country"]
        )


class PrivateManufacturerUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_password_123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_update_view_response_with_correct_template(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.get(
            reverse(MANUFACTURER_UPDATE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_update_view_has_correct_success_url(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.get(
            reverse(MANUFACTURER_UPDATE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(
            response.context_data["view"].success_url,
            MANUFACTURER_LIST_URL
        )

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.post(reverse(
            MANUFACTURER_UPDATE_URL, kwargs={"pk": manufacturer.id}
        ),
            {"name": "updated_name", "country": "updated_country"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=1).name,
            "updated_name"
        )


class PrivateManufacturerDeleteViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_delete_view_has_correct_template__success_url(self):
        manufacturer = Manufacturer.objects.get(id=1)
        response = self.client.get(
            reverse(MANUFACTURER_DELETE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )
        self.assertEqual(
            response.context_data["view"].success_url,
            MANUFACTURER_LIST_URL
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        response = self.client.post(
            reverse(MANUFACTURER_DELETE_URL, kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
