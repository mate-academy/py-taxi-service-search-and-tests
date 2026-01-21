from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword3"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="Qwerty123",
            license_number="TES12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver license number on the admin page is listed
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_listed(self):
        """
        Test that driver license number on the admin detail page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
