from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from django.urls import reverse


class AdminPanelTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA11111",
            first_name="test_first",
            last_name="test_last",
        )

    def test_admin_panel_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_admin_panel_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_admin_panel_has_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "Additional info")
        self.assertContains(res, "license_number")
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
