from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPageTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin_test",
            password="1234"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="1234",
            license_number="ABC23456"
        )
        self.client.force_login(self.admin)

    def test_driver_license_number_listed(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_in_updating_form(self):
        url = "admin:taxi_driver_change"
        response = self.client.get(reverse(url, args=[self.driver.id]))
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_in_creating_form(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertContains(
            response,
            'input type="text" name="license_number"'
        )
