from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = (
            get_user_model()
            .objects
            .create_superuser(
                username="new_user",
                password="password_test"
            )
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="pass_test",
            first_name="first_name_test",
            last_name="last_name_test",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_creation_license_number(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(
            res, self.driver._meta.get_field(
                "license_number").name)
