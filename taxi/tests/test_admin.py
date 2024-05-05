from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test driver",
            license_number="test license number",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver`s license is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist", )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver`s license is in list_display on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
