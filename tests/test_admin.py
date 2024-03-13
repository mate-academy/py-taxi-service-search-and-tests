from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
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
            license_number="TES12345"
        )

    def test_driver_license_listed(self) -> None:
        """
        Test that driver license is listed in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_listed(self) -> None:
        """
        Test that driver license is listed in on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_add_fieldsets(self) -> None:
        """
        Test that add_fieldsets includes the necessary fields
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "license_number")
