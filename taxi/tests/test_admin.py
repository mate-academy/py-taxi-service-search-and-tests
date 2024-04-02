from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
            license_number="AAA12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that user's license number is in list_display on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that user's license number is in on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)
