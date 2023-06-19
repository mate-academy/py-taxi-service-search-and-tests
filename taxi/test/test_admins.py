from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.obj_driver = get_user_model().objects.create_user(
            username="user321",
            first_name="user_first",
            last_name="user_last",
            password="user12345",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.obj_driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.obj_driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.obj_driver.license_number)

    def test_driver_add_additional_info(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")
