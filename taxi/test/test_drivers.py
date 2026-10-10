from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class DriverSearchTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="ivan", password="pass", license_number="ABC12345"
        )
        User.objects.create_user(
            username="ivanov", password="pass", license_number="DEF12345"
        )
        User.objects.create_user(
            username="peter", password="pass", license_number="HTY12345"
        )
        self.client.force_login(User.objects.get(username="ivan"))

    def test_search_by_username(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url, {"username": "ivan"})
        self.assertEqual(resp.status_code, 200)
        qs = resp.context.get("driver_list")
        self.assertEqual(len(qs), 2)
        usernames = [u.username for u in qs]
        self.assertIn("ivan", usernames)
        self.assertIn("ivanov", usernames)
