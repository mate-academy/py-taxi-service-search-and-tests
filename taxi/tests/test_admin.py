from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="Bob",
            password="123"
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            username="Max",
            password="123",
            email="max@gamil.com",
            first_name="max",
            last_name="tibon",
            is_staff=False,
            license_number="SDC77233"
        )

    def test_driver_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)
