from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )

        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number is in list_display
        on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        :return:
        """
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_add_license_number_field(self):
        """
        Test that the 'license_number' field is included on the driver add page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, 'name=\"first_name\"')
        self.assertContains(response, 'name=\"last_name\"')
        self.assertContains(response, 'name=\"license_number\"')
