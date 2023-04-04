from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="TestAdmin", password="TestPass12345"
        )
        self.client.force_login(self.user_admin)
        self.driver = get_user_model().objects.create_user(
            username="TestDriver",
            password="TestDriverPass1232134125",
            license_number="TST45451",
        )

    def test_driver_license_num_in_list(self):
        """Tests that license_number is listed on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_num_in_list(self):
        """Tests that license_number is listed on driver-detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)
