from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testadmin"
        )
        self.client.force_login(user=self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="testadriver", license_number="GOR13112"
        )

    def test_driver_license_number_listed(self):
        """
        Test that license number is in list_display on driver page
        ;return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
