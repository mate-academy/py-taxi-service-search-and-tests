from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="TEST8292"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver license number is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver license number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_add_fieldsets_listed(self):
        """
        Test that driver license number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])

        res = self.client.post(
            url,
            {
                "first_name": "Test_first_name",
                "last_name": "Test_last_name",
                "license_number": "TEST1111"
            }
        )

        self.assertContains(res, "Test_first_name")
        self.assertContains(res, "Test_last_name")
        self.assertContains(res, "TEST1111")
