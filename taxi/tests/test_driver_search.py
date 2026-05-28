from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class DriverSearchFormTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="john_driver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="JOH12345",
        )

        self.driver2 = get_user_model().objects.create_user(
            username="mike",
            password="test12345",
            first_name="Mike",
            last_name="Smith",
            license_number="MIK12345",
        )

    # 1. Пошук по username (основний кейс)
    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]

        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_driver")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "not_exists"}
        )

        drivers = response.context["driver_list"]

        self.assertEqual(len(drivers), 0)

    # 4. Case insensitive search
    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"}
        )

        drivers = response.context["driver_list"]

        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_driver")

    # 5. Частковий збіг
    def test_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        drivers = response.context["driver_list"]

        self.assertTrue(
            all("john" in driver.username.lower() for driver in drivers)
        )

    # 6. Перевірка, що view доступний (200 + auth)
    def test_driver_list_view_status_code(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)

    # 7. Redirect якщо не залогінений
    def test_redirect_if_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 302)
