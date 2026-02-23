from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="testadmin",
            password="test1234",
            license_number="ABC12345"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="Anton",
            password="anton_narkoman",
            license_number="ANT12345"
        )

    def test_test_driver_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_test_detail_driver_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
