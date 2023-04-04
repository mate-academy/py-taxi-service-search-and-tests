from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPageTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="user.admin",
            password="password123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="passusertest",
            first_name="Test_first",
            last_name="Test_last",
            license_number="ZXC12345",
        )

    def test_show_license_number_list(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_show_detailed_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_show_manufacturer_list(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
