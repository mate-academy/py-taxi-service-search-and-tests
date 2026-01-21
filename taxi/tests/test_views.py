from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[1])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[1])
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
PAGINATION = 5


class PublicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        protected_urls = [
            INDEX_URL,
            DRIVER_LIST_URL,
            DRIVER_DETAIL_URL,
            DRIVER_CREATE_URL,
            DRIVER_UPDATE_URL,
            DRIVER_DELETE_URL,
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)


class ManufacturerListTest(TestCase):
    fixtures = [
        "taxi_service_db_data.json",
    ]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_response_with_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_paginated_correctly(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(
            len(response.context["manufacturer_list"]), PAGINATION
        )

    def test_manufacturer_list_ordered_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        man_list = Manufacturer.objects.all().order_by("name")
        manufacturer_context = response.context["manufacturer_list"]

        self.assertEqual(
            list(manufacturer_context),
            list(man_list[: len(manufacturer_context)]),
        )
