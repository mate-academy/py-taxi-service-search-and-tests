from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="TestPassword",
            license_number="TS123456"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number
        is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_creation_additional_fields_listed(self):
        """
        Test that driver's first_name, last_name and license number
        is on driver creation admin page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "License number")
