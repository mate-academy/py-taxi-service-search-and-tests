from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            license_number="ASD39042",
            first_name="John",
            last_name="Black",
            password="driverpassword",
        )

    def test_driver_license_number_listed(self):
        """
        Tests that license number is in list_display on driver admin page
        """

        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """
        Tests that license number is displayed on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver(self):
        """
        Tests that license number is displayed on driver detail admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "Additional info")
