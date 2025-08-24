from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="testdriver",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)

    def test_author_detail_pseudonym_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.license_number)
