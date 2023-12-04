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
            username="author",
            password="testdriver1",
            license_number="ADM77777"
        )

    def test_driver_license_number_listed(self) -> None:
        """Test that driver's license_number is in list_display
        on driver admin page """
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        """Test that driver's license_number is on detail admin page """
        url = reverse("admin:taxi_driver_change",
                      args=[self.driver.id])
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)
