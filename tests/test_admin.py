from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="testadmin",
            password="testpass",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="TES12121",
        )

    def test_driver_license_in_list_display(self):

        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_in_detail_view(self):

        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
