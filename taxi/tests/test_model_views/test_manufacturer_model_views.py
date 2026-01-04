from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from . import utils

APP_NAME = "taxi"
MODEL = Manufacturer
MODEL_FIELDS = ("name", "country")
UNIQUE_FIELDS = ("name", )
NON_RELATIONAL_FIELDS = ("name", "country")
FOREIGN_KEY_FIELDS = {}
MANY_TO_MANY_FIELDS = {}

MODEL_NAME = MODEL.__name__.lower()
RELATIONAL_FIELDS = {
    "foreign_relation": FOREIGN_KEY_FIELDS,
    "many_relation": MANY_TO_MANY_FIELDS,
}
# Parameters that will be passed to the instance creation functions.
# Don't change the order!
CREATION_PARAMS = (
    MODEL, NON_RELATIONAL_FIELDS, RELATIONAL_FIELDS, UNIQUE_FIELDS
)

LIST_URL = f"{APP_NAME}:{MODEL_NAME}-list"
DETAIL_URL = f"{APP_NAME}:{MODEL_NAME}-detail"
CREATE_URL = f"{APP_NAME}:{MODEL_NAME}-create"
UPDATE_URL = f"{APP_NAME}:{MODEL_NAME}-update"
DELETE_URL = f"{APP_NAME}:{MODEL_NAME}-delete"


class ManufacturerListViewPublicTest(TestCase):
    def test_manufacturer_list_view_is_private(self):
        response = self.client.get(reverse(LIST_URL))
        self.assertNotEqual(response.status_code, 200)


class ManufacturerListViewPrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        utils.bulk_create_model_instances(*CREATION_PARAMS)

    def setUp(self):
        self.user = utils.create_user_object()
        self.client.force_login(self.user)
        self.url = reverse(LIST_URL)
        self.response = self.client.get(self.url)
        self.num_per_page = self.response.context["paginator"].per_page
        self.search_fields = self.response.context["search_form"].fields.keys()
        self.search_data = "test2"
        self.view_type = "list"
        self.context_name = utils.build_context_name(
            MODEL_NAME, self.view_type
        )
        self.template = f"{APP_NAME}/{self.context_name}.html"

    def test_manufacturer_list_view_is_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, self.template)

    def test_manufacturer_list_view_pagination_is_correct(self):
        self.assertTrue(self.response.context["is_paginated"])
        self.assertEqual(
            len(self.response.context[self.context_name]),
            self.num_per_page
        )

    def test_manufacturer_list_view_displays_all_items(self):
        num_pages = self.response.context["paginator"].num_pages
        response = self.client.get(self.url + f"?page={num_pages}")
        self.assertEqual(
            len(response.context[self.context_name]),
            MODEL.objects.count() - self.num_per_page * (num_pages - 1)
        )

    def test_manufacturer_list_view_search_displays_correct_results(self):
        # Make sure that you don't expect the search to return more results
        # than is specified in pagination for one page.
        for field in self.search_fields:
            response = self.client.get(
                self.url + f"?{field}={self.search_data}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.context[self.context_name]),
                MODEL.objects.filter(
                    **{f"{field}__icontains": self.search_data}
                ).count()
            )

    def test_manufacturer_list_view_context_is_correct(self):
        for field in self.search_fields:
            response = self.client.get(
                self.url + f"?{field}={self.search_data}"
            )
            self.assertIn("search_form", response.context)
            form = response.context["search_form"]
            self.assertEqual(form.initial.get(field), self.search_data)


class ManufacturerCreateViewPublicTest(TestCase):
    def test_manufacturer_create_view_is_private(self):
        response = self.client.get(reverse(CREATE_URL))
        self.assertNotEqual(response.status_code, 200)


class ManufacturerCreateViewPrivateTest(TestCase):
    def setUp(self):
        self.user = utils.create_user_object()
        self.client.force_login(self.user)
        self.url = reverse(CREATE_URL)
        self.response = self.client.get(self.url)
        if relational_fields := FOREIGN_KEY_FIELDS | MANY_TO_MANY_FIELDS:
            utils.create_related_objects(relational_fields)

    def test_manufacturer_create_view_is_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_create_view_contains_all_fields(self):
        form = self.response.context.get("form")
        for field in MODEL_FIELDS:
            self.assertIn(field, form.fields)

    def test_manufacturer_create_view_redirect_is_correct(self):
        post_data = utils.fill_out_create_update_forms(
            "Test", NON_RELATIONAL_FIELDS, RELATIONAL_FIELDS
        )
        response_post = self.client.post(self.url, post_data)
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse(LIST_URL))


class ManufacturerUpdateViewPublicTest(TestCase):
    def test_manufacturer_update_view_is_private(self):
        utils.create_model_instance(*CREATION_PARAMS)
        url = reverse(UPDATE_URL, kwargs={"pk": MODEL.objects.first().pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class ManufacturerUpdateViewPrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        utils.create_model_instance(*CREATION_PARAMS)

    def setUp(self):
        self.user = utils.create_user_object()
        self.client.force_login(self.user)
        self.url = reverse(UPDATE_URL, kwargs={"pk": MODEL.objects.first().pk})
        self.response = self.client.get(self.url)

    def test_manufacturer_update_view_is_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_update_view_contains_all_fields(self):
        form = self.response.context.get("form")
        for field in MODEL_FIELDS:
            self.assertIn(field, form.fields)

    def test_manufacturer_update_view_redirect_is_correct(self):
        post_data = utils.fill_out_create_update_forms(
            "Updated", NON_RELATIONAL_FIELDS, RELATIONAL_FIELDS
        )
        response_post = self.client.post(self.url, post_data)
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse(LIST_URL))


class ManufacturerDeleteViewPublicTest(TestCase):
    def test_manufacturer_delete_view_is_private(self):
        utils.create_model_instance(*CREATION_PARAMS)
        url = reverse(DELETE_URL, kwargs={"pk": MODEL.objects.first().pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class ManufacturerDeleteViewPrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        utils.create_model_instance(*CREATION_PARAMS)

    def setUp(self):
        self.user = utils.create_user_object()
        self.client.force_login(self.user)
        self.url = reverse(DELETE_URL, kwargs={"pk": MODEL.objects.first().pk})
        self.response = self.client.get(self.url)

    def test_manufacturer_delete_view_is_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_delete_view_redirect_is_correct(self):
        response_post = self.client.post(self.url, {})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse(LIST_URL))
