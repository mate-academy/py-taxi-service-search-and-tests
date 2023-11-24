from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admintestuser",
            password="admintestpass",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword12",
            license_number="AGY12345"
        )

    def test_user_list_display(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_fieldset(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)

    def test_driver_creation_page_fieldset(self) -> None:
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
