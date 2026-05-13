from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin")
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            first_name="firstTest",
            last_name="lastTest",
            password="driverpassword",
            license_number="driverlicense")

    def test_driver_license_number_listed(self):
        """
        Test that the driver license_number listed in the admin panel
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that the driver detail license_number listed in the admin panel
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_author_add_changelist(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "license_number")
        self.assertContains(res, "Additional info")
