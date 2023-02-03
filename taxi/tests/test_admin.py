from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="author12345",
            license_number="MAT44444"
        )

    def test_drivers_license_number_listed(self):
        """
        Test that driver's license number is shown at the driver's admin panel
        """

        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_detailed(self):
        """
        Test that driver's lisense number is shown
        at the driver's detail admin page
        """

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)
