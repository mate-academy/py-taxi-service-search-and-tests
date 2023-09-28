import math

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.views import DriverListView

DRIVER_LIST_URL = reverse("taxi:driver-list")


class TestSearch(TestCase):
    def setUp(self) -> None:
        drivers = []
        for i in range(8):
            driver = get_user_model().objects.create_user(
                username=f"driver{i}",
                license_number=f"AAA0000{i}",
                first_name=f"Name{i}",
                last_name=f"Last{i}",
                password=f"1q2Aafdojpass{i}",
            )
            drivers.append(driver)
        self.drivers = drivers
        self.client.force_login(drivers[0])

    def test_view_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_empty_search_return_all_data(self):
        form_data = {"username": ""}
        per_page = DriverListView.paginate_by
        total_pages = math.ceil(len(self.drivers) / per_page)

        url = DRIVER_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context
        queryset = context["driver_list"]

        self.assertEqual(queryset.count(), per_page)
        self.assertTrue(context["is_paginated"])
        self.assertEqual(
            str(context["page_obj"]), f"<Page 1 of {total_pages}>"
        )

    def test_search_should_return_all_matches_despite_register(self):
        form_data = {"username": "E"}
        per_page = DriverListView.paginate_by
        total_pages = math.ceil(len(self.drivers) / per_page)

        url = DRIVER_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context
        queryset = context["driver_list"]

        self.assertEqual(queryset.count(), per_page)
        self.assertTrue(context["is_paginated"])
        self.assertEqual(
            str(context["page_obj"]), f"<Page 1 of {total_pages}>"
        )

    def test_search_should_return_nothing_if_no_matches(self):
        form_data = {"username": f"driver{len(self.drivers)}"}

        url = DRIVER_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context
        queryset = context["driver_list"]

        self.assertEqual(queryset.count(), 0)

    def test_should_return_correst_user_on_exact_username_input(self):
        form_data = {"username": "driver5"}

        url = DRIVER_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context
        queryset = context["driver_list"]

        self.assertEqual(queryset.count(), 1)
