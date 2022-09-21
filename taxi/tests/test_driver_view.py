from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse

from taxi.models import Driver
from taxi.views import DriverListView

DRIVER_LIST_URL = reverse("taxi:driver-list")


class TestDriver(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="driver1234"
        )
        self.client.force_login(self.driver)
        num_drivers = 8
        for num in range(num_drivers):
            form_data = {
                "username": f"username_{num}",
                "password1": f"test12345{num}",
                "password2": f"test12345{num}",
                "first_name": f"First_name{num} test",
                "last_name": f"Last_name{num} test",
                "license_number": f"AAA1234{num}"
            }
            self.client.post(reverse("taxi:driver-create"), data=form_data)

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/drivers/")

    def test_private_permission(self):
        resp = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/driver_list.html")

    def test_retrieve_drivers_pagination_5(self):
        resp = self.client.get(DRIVER_LIST_URL)

        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertEqual(len(resp.context["driver_list"]), 5)

    def test_second_page_paginated(self):
        resp = self.client.get(DRIVER_LIST_URL + "?page=2")

        self.assertEqual(len(resp.context["driver_list"]), 4)

    def test_detail_page(self):
        driver_2 = Driver.objects.get(id=2)
        resp = self.client.get(reverse("taxi:driver-detail", kwargs={"pk": driver_2.id}))
        self.assertContains(resp, driver_2.first_name)
        self.assertContains(resp, driver_2.last_name)
        self.assertContains(resp, driver_2.license_number)

    def test_search_queryset_driver(self):
        request = RequestFactory().get("?username=username_1")
        view = DriverListView()
        view.request = request
        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Driver.objects.filter(username__icontains="username_1"))
