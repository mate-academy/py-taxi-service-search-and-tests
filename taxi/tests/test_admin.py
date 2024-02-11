from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="AAA12345"
        )

    def test_driver_license_listed(self):
        """
        Test that driver's license is in list_display on admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=(self.driver.pk,))
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)