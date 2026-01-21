from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminPanelTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            license_number="TES12345"
        )
        self.client.force_login(self.admin_user)

    def test_driver_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.admin_user.license_number)
