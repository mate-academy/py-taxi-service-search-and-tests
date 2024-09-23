from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class DriverViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword456",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def create_drivers(self, instance_count):
        for counter in range(10, instance_count + 10):
            get_user_model().objects.create_user(
                username=f"usertest{counter}",
                password=f"testpassword456{counter}",
                license_number=f"ABC123{counter}",
            )

    def test_login_required_views(self):
        login_required_urls = [
            reverse_lazy("taxi:driver-list"),
            reverse_lazy("taxi:driver-create"),
            reverse_lazy("taxi:driver-detail", args=[1]),
            reverse_lazy("taxi:driver-update", args=[1]),
            reverse_lazy("taxi:driver-delete", args=[1]),
        ]

        for url in login_required_urls:
            self.client.logout()

            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)
            expected_url = f"/accounts/login/?next={url}"
            self.assertRedirects(response, expected_url)

            self.client.force_login(self.driver)
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_driver_list_view_pagination(self):
        self.create_drivers(10)
        response = self.client.get(reverse_lazy("taxi:driver-list"))

        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["driver_list"]) == 5)

    def test_driver_list_view_search(self):
        self.create_drivers(10)
        response = self.client.get(
            reverse_lazy("taxi:driver-list"), {"search": "testuser"}
        )

        self.assertContains(response, self.driver.username)
        self.assertTrue(len(response.context["driver_list"]) == 1)

        response = self.client.get(
            reverse_lazy("taxi:driver-list"), {"search": "usertest"}
        )

        self.assertTrue(len(response.context["driver_list"]) == 5)

    def test_driver_list_view_not_result_search(self):
        self.create_drivers(10)
        response = self.client.get(
            reverse_lazy("taxi:driver-list"), {"search": "qwerty"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["driver_list"])

    def test_driver_list_view_empty_search(self):
        self.create_drivers(10)
        response = self.client.get(
            reverse_lazy("taxi:driver-list"), {"search": ""}
        )

        self.assertTrue(len(response.context["driver_list"]) == 5)

    def test_driver_list_view_search_form_saves_get_parameters(self):
        response = self.client.get(
            reverse_lazy("taxi:driver-list"),
            {"search": "usertest", "color": "blue"}
        )
        self.assertContains(
            response, '<input type="hidden" name="color" value="blue">'
        )
        self.assertNotContains(response, '<input type="hidden" name="search"')

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse_lazy("taxi:driver-detail", args=[self.driver.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)

    def test_driver_delete_view(self):
        response = self.client.get(
            reverse_lazy("taxi:driver-detail", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse_lazy("taxi:driver-delete", args=[self.driver.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )

    def test_create_driver_view(self):
        form_data = {
            "username": "username",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "QWE12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        self.assertFalse(
            get_user_model().objects.filter(
                username=form_data["username"]
            ).exists()
        )

        response = self.client.post(
            reverse_lazy("taxi:driver-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(
                username=form_data["username"]
            ).exists()
        )

    def test_update_driver_view(self):
        form_data = {
            "license_number": "QWE54321",
        }

        self.assertFalse(
            get_user_model()
            .objects.filter(license_number=form_data["license_number"])
            .exists()
        )

        response = self.client.post(
            reverse_lazy("taxi:driver-update", args=[self.driver.pk]),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model()
            .objects.filter(license_number=form_data["license_number"])
            .exists()
        )
