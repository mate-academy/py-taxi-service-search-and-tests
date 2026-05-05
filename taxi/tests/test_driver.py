from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="Alex_Driver",
            email="alex@gmail.com",
            password="password123",
            license_number="ABC98765",
        )

        self.user2 = get_user_model().objects.create_user(
            username="best_driver",
            email="best@gmail.com",
            password="pass98312",
            license_number="ABC92321",
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="",
            password="password",
            license_number="ABC12345",
        )

    def test_driver_search(self):
        self.client.force_login(self.admin_user)

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "Alex_Driver"})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Alex_Driver")
        self.assertNotContains(response, "best_driver")

        drivers = response.context["driver_list"]
        self.assertIn(self.user1, drivers)
        self.assertNotIn(self.user2, drivers)
        self.assertNotIn(self.admin_user, drivers)

    def test_search_driver_all(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""}
        )

        self.assertContains(response, "Alex_Driver")
        self.assertContains(response, "best_driver")

    def test_search_no_results_driver(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "NonExistent"}
        )

        self.assertEqual(len(response.context["driver_list"]), 0)
