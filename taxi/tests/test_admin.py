from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="userTom",
            password="pass1234",
            license_number="ASD12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_add_fieldsets_listed(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "license_number")
