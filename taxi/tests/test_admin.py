from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="paSSword",
            license_number="AAA12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that license number is listed as expected.
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that license number is on driver detail admin page.
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fields_listed(self):
        """
        Test that fields are listed as expected.
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
