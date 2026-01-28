from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class DriverAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver_admin = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
        )
        self.client.force_login(self.driver_admin)

        self.driver = get_user_model().objects.create_user(
            username="user",
            password="password1",
            license_number="TES12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number is
        in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_add_new_driver_with_additional_info(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Additional info")

        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="license_number"')
