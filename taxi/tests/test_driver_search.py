from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1",
            license_number="TRT12345"
        )
        self.client.force_login(self.user)
        User.objects.create_user(
            username="john",
            password="pass",
            license_number="TER12345"
        )
        User.objects.create_user(
            username="jane",
            password="pass",
            license_number="TST34567"
        )
        User.objects.create_user(
            username="doe",
            password="pass",
            license_number="TST23456"
        )
        User.objects.create_user(
            username="jason",
            password="pass",
            license_number="TSN34567"
        )

    def test_search_by_username_returns_matching_users(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=jan"
        )

        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(len(object_list), 1)
        usernames = [u.username for u in object_list]
        self.assertEqual(set(usernames), {"jane"})

    def test_search_by_username_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=JAN"
        )

        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(len(object_list), 1)
        usernames = [u.username for u in object_list]
        self.assertEqual(set(usernames), {"jane"})

    def test_search_by_username_multiple_matches(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=ja"
        )

        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(len(object_list), 2)
        usernames = [u.username for u in object_list]
        self.assertEqual(set(usernames), {"jane", "jason"})
