from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdmitSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="andin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            first_name="test_first",
            last_name="test_last",
            license_number="TEST123",
        )

    def test_driver_list_licence_number(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_list_licence_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_add_driver_list_info(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
