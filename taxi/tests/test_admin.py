from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="qwerty"
        )

        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="AlexKing",
            password="qwerty12345",
            first_name="Alex",
            last_name="Smith",
            license_number="KMZS12345",
        )

    def test_driver_changelist_page(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)
        self.assertContains(response, self.driver.license_number)

    def test_driver_change_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_driver_add_page(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
