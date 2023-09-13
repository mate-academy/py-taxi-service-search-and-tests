from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminTests(TestCase):

    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="adminds",
            password="admin12sd34",
            license_number="DSA12321"
        )

    def test_driver_pseudonym_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_author_detail_pseudonym_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
