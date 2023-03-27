from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser12345",
            license_number="ABC12345",
        )

    def test_license_number_is_displayed_in_driver_list(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.license_number)

    def test_license_number_is_displayed_in_driver_detailed_view(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertContains(res, self.user.license_number)
