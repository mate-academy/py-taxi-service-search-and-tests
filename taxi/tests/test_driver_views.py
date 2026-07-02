from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="TST12345",
        )

    def test_page_available_for_logged_in_user(self):
        self.client.force_login(self.user)
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_driver_search_by_username(self):
        self.client.force_login(self.user)
        first_driver = get_user_model().objects.create_user(
            username="john_driver",
            password="test_password",
            license_number="JHN12345",
        )
        second_driver = get_user_model().objects.create_user(
            username="bob_driver",
            password="test_password",
            license_number="BOB12345",
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})

        self.assertContains(response, first_driver.username)
        self.assertNotContains(response, second_driver.username)
