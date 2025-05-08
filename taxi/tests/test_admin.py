from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdminSite(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin123",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver123",
            license_number="TES12345",
        )

    def test_drivers_license_number_listed(self):
        """
        Test that the driver's license number is
        in the list_display on the admin page.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_drivers_detail_license_number_listed(self):
        """
        Test that the driver's license number is
        in the detail on the admin page.
        """
        url = reverse(
            "admin:taxi_driver_change", args=[self.driver.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_form_fields_displayed(self):
        """
        Test that the driver's license number, first name
        and last name are added to the driver admin page.
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="license_number"')
