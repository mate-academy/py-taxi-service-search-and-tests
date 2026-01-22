from http import client

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="TEST1234",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="TEST1234",
            license_number="TES12345",
            first_name="testfirst",
            last_name="testsecond",
        )

    def test_driver_license_number_listed(self):
        """
        Test that the driver license number is listed in the admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that the driver license number is in driver detail admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
