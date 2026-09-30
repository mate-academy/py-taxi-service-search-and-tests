from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.tests.base import LoggedInTestCase

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateDriverViewsTest(LoggedInTestCase):
    def test_list_search_by_username(self):
        get_user_model().objects.create_user(
            username="alice", password="test12345", license_number="AAA11111"
        )
        get_user_model().objects.create_user(
            username="bob", password="test12345", license_number="BBB22222"
        )

        response = self.client.get(DRIVER_LIST_URL, {"searched_value": "ALI"})

        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "alice")

    def test_create_driver(self):
        data = {
            "username": "new_driver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "DDD44444",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.client.post(reverse("taxi:driver-create"), data)

        self.assertTrue(
            get_user_model().objects.filter(username="new_driver").exists()
        )

    def test_update_license(self):
        url = reverse("taxi:driver-update", args=[self.user.pk])
        response = self.client.post(url, {"license_number": "XYZ98765"})

        self.assertRedirects(response, DRIVER_LIST_URL)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "XYZ98765")

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="to_delete",
            password="test12345",
            license_number="CCC33333",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", args=[driver.pk])
        )

        self.assertRedirects(response, DRIVER_LIST_URL)
        self.assertFalse(
            get_user_model().objects.filter(pk=driver.pk).exists()
        )
