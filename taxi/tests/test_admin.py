from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin1234",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver1234",
            license_number="ABC12345",
        )

    def test_driver_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_list_display(self):
        url = reverse("admin:taxi_driver_changelist", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
