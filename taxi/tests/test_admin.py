from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="<PASSWORD>",
            license_number="AAA11111"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number is listed in admin page.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is listed in detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_first_name_listed(self):
        """
        Test that driver's first_name is listed in detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)

    def test_driver_detail_last_name_listed(self):
        """
        Test that driver's last name is listed in detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.last_name)
