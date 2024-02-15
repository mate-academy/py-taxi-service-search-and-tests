from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.driver = get_user_model().objects.create(
            username="user_test",
            password="passwordtest",
            license_number="AAA12345"
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        expected_fields = ["first_name", "last_name", "license_number"]

        for field in expected_fields:
            self.assertContains(response, field)
