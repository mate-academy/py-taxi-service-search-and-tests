from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="TST12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test driver's license number is in list_display on driver admin page.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test driver's license number is on driver detail admin page.
        """
        url = reverse("admin:taxi_driver_change",
                      args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_added_fieldsets_listed(self):
        """
        Test driver's license number,
        first name and last name are on
        driver detail admin page.
        """
        url = reverse("admin:taxi_driver_change",
                      args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
