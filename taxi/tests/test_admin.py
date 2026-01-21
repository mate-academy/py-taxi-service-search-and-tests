from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="123123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_superuser(
            username="driver",
            password="11111111",
            license_number="AAA17171"
        )

    def test_driver_license_number(self):
        """
        Test that driver's license number is in list_display on driver
        admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number(self):
        """
        Test that driver's license number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
