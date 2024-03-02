from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin2", password="Admin1991"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="test_username", password="testpassword1991", license_number="ABC12345"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_license__listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)
