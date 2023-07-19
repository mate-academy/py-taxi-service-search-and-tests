from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin12",
            password="admin123456",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="author123456",
            license_number="BBB12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_field(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
