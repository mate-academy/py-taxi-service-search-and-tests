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
            license_number="JIM26556",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver`s license_number is in list_display
        an driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver`s license_number is an driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        """
        Теые that the driver's license number is the admin page
        about adding a driver.
        """
        url = reverse("admin:taxi_driver_add")
        data = {
            "username": "new_driver",
            "license_number": "JIM26556",
        }
        res = self.client.get(url, data)
        self.assertContains(res, data["license_number"])
