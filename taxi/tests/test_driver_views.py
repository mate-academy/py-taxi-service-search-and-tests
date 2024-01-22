from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverUsernameSearchForm
from taxi.models import Driver


class DriverViewsTest(TestCase):
    DRIVER_LIST_URL = reverse("taxi:driver-list")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
            password="testpassword",
        )

        self.client = Client()
        self.client.force_login(self.user)
        for _id in range(15):
            Driver.objects.create(
                username=f"testuser {_id}",
                license_number=f"ABC123{_id}",
                password="testpassword",
            )

    def test_list_if_not_login(self):
        self.client.logout()
        res = self.client.get(self.DRIVER_LIST_URL)
        self.assertRedirects(res, "/accounts/login/?next=/drivers/")

    def test_list_view_if_logged_in(self):
        res = self.client.get(self.DRIVER_LIST_URL)

        self.assertEqual(str(res.context["user"]), str(self.user))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_list_view_pagination(self):
        res = self.client.get(self.DRIVER_LIST_URL)

        self.assertTrue("is_paginated" in res.context)
        self.assertEqual(len(res.context["driver_list"]), 5)

    def test_list_view_search(self):
        driver = Driver.objects.create(
            username="danylo",
            password="testpassword",
        )
        res = self.client.get("/drivers/?username=dan")

        self.assertTrue("search_form" in res.context)
        self.assertIsInstance(
            res.context["search_form"],
            DriverUsernameSearchForm
        )
        self.assertEqual(
            res.context["search_form"].initial["username"], "dan")
        self.assertEqual(len(res.context["driver_list"]), 1)
        self.assertEqual(res.context["driver_list"][0], driver)

    def test_list_view_invalid_search(self):
        res = self.client.get("/drivers/?name=")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 5)
        self.assertFalse(res.context["search_form"].is_valid())
