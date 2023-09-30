from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123456"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="password354321",
            license_number="HJU78945",
        )

    def test_driver_license_number(self):
        """
        Test whether the license number is displayed on the admin page
        """

        url = "http://127.0.0.1:8000/admin/taxi/driver/"
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_in_detail(self):
        """
        Test that driver's licence_number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
