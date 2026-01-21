from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_admin = get_user_model().objects.create_superuser(
            username="admin",
            password="Admin123!",
        )
        self.client.force_login(self.new_admin)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="Test123!",
            license_number="ABC12345"
        )

    def test_the_driver_licence_field_is_exists(self):
        """
        Test if the driver license column listed in admin panel
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
