from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

URLS = [
    reverse("taxi:index"),
    reverse("taxi:car-list"),
    reverse("taxi:manufacturer-list"),
    reverse("taxi:driver-list"),
]


class PublicViewsTest(TestCase):
    def test_login_required(self):
        for url in URLS:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_superuser(
            username="user.admin",
            license_number="ADM00000",
            first_name="Admin",
            last_name="Admin",
            password="1q2Aafdojpass",
        )
        self.client.force_login(user)

    def test_access_gained_if_login(self):
        for url in URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
