from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="admintest",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="drivertest",
            license_number="test_license",
        )

    def test_driver_license_listed(self) -> None:
        """
        Tests if driver license number is displayed
        on driver list admin page.
        """

        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_license_listed(self) -> None:
        """
        Tests if driver license number is displayed
        on driver detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)
