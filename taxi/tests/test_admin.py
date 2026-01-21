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
            license_number="Test License",
        )

    def test_driver_license_number_listed(self):
        """
        Test that license number is listed on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that license number is listed on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_creation_page_contains_license_number_field(self):
        """
        Test that driver creation page contains license
        number field in the additional info section
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
