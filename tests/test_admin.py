from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="ADM56984",
        )

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver`s pseudonym is in list_display
        on driver detail admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_listed(self):
        """
        Test that driver`s pseudonym is in list_display
        on driver admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_in_add_fieldsets(self):
        """
        Test that driver`s license_number is in add_fieldsets
         on driver admin page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, '<input type="text" name="license_number"')
