from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="user",
            password="u1s2e3r4"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_superuser(
            username="jo_er",
            password="z1x2c3v4",
            license_number="JUY44831"
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
