from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="pass12345word",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="password12345",
            license_number="ASD12345"
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license number is
         in ist_display on driver admin page"""

        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Test that driver's license number is on driver detail admin page"""

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_add_new_driver(self):
        """Test that driver's first name, last name and
        license number is on add driver admin page"""

        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "First name:")
        self.assertContains(res, "Last name:")
        self.assertContains(res, "License number:")
