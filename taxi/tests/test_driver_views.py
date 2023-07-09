from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverViewTest(TestCase):

    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=/drivers/")


class PrivateDriverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for driver_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_user_{driver_id}",
                password=f"test_test_test_{driver_id}",
                license_number=f"ADM1234{driver_id}"
            )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get("/drivers/")

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_correct_pagination_on_first_page(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["driver_list"]), 5)

    def test_correct_pagination_on_second_page(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["driver_list"]), 4)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123user",
            "password2": "user123user",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "TES12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
