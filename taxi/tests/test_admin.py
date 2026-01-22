from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="QWE12345",
        )

    def test_license_number(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.user.pk])
        res = self.client.get(url)

        self.assertContains(res, self.user.license_number)

    def test_driver_list(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.license_number)
