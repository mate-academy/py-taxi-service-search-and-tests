from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123password",
            license_number="TST12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license_number is in list_display
        on driver's admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_additional_info_listed(self):
        """
        Test that driver's Additional Info is on driver's detail admin page
        """
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, "Additional info")
        self.assertContains(response, "fields")
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)
