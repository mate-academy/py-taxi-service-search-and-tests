from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_check",
            password="Testuser123",
            license_number="ERT12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test thant driver's license_number is in list_display on admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test thant driver's license_number is in on admin detail page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_additional_detail_license_number_listed(self):
        """
        Test thant driver's license_number
        is in on admin additional detail page
        :return:
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertTrue(res, self.driver.license_number)
