from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC123456",
            password="testpassword",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver`s license_number is in list_display
        on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_admin_detail_license_number_listed(self):
        """
        Test that driver`s license_number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_admin_add_license_number_listed(self):
        """
        Test that driver`s license_number is on driver add admin page
        :return:
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "License number")
