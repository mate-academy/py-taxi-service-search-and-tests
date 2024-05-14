from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testdriver",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number
                                is in list_display on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets_listed(self):
        """
        Test that the correct fields are displayed in the 'Additional info'
        fieldset when adding a new driver in the admin site.
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "Additional info")

        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")
