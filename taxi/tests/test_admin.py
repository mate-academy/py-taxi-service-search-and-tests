from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TaxiAdminTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="test_admin", password="123Admin"
        )

        self.client = Client()
        self.client.force_login(self.admin)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number",
        )

    def test_admin_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_admin_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_admin_add_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)
        self.assertContains(response, self.driver.license_number)
