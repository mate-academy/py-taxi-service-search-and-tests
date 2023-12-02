from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testAdmin12",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="testDriver12",
            license_number="TST12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver`s license number is in list_display
        on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver`s license number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
