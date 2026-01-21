from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVERS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

        number_of_drivers = 10
        for driver_id in range(1, number_of_drivers):
            Driver.objects.create(
                username=f"User{driver_id}",
                password=f"Password{driver_id}",
                first_name=f"First{driver_id}",
                last_name=f"Last{driver_id}",
                license_number=f"LIC{driver_id}2345"
            )

    def test_create_driver(self):
        form_data = {
            "username": "User_user",
            "password1": "passwordtest",
            "password2": "passwordtest",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "USE12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVERS_URL)
        drivers = Driver.objects.all()[:5]
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(DRIVERS_URL)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_logged_in_access(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_query_search_filter(self):
        response = self.client.get(f"{DRIVERS_URL}?username=User1")
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="User1")
        )
