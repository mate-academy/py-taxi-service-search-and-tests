from django.contrib.auth import get_user_model
from django.template.defaultfilters import urlencode
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver


class TestManufacturerViewList(TestCase):
    def setUp(self):
        number_of_manufacturers = 15

        for i in range(number_of_manufacturers):
            Manufacturer.objects.create(name=f"test{i}", country=f"test{i}")

        self.user = get_user_model().objects.create(
            username="test", password="test1234"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_search_field(self):
        self.client.force_login(self.user)
        base_url = reverse("taxi:manufacturer-list")
        query_params = {"name": 5}
        url = f"{base_url}?{urlencode(query_params)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context["object_list"])), 2)


class TestDriverViewList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test", password="test1234", license_number="QWE12345"
        )

        get_user_model().objects.create(
            username="test2", password="test2234", license_number="QWE23456"
        )

        get_user_model().objects.create(
            username="test3", password="test3234", license_number="QWE34567"
        )

        get_user_model().objects.create(
            username="test4", password="test3234", license_number="QWE45678"
        )

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_search_field(self):
        self.client.force_login(self.user)
        base_url = reverse("taxi:driver-list")
        query_params = {"username": "2"}
        url = f"{base_url}"
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
