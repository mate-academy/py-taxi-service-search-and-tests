from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class DriverAdminTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            license_number="XYZ12345"
        )

    def test_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_license_number_in_detail_view(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)

    def test_add_driver_page_contains_license_number(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")

    def test_regular_user_cannot_access_admin(self):
        self.client.logout()
        self.client.force_login(self.driver)
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_create_driver_without_license_number(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.post(url, {
            "username": "newdriver",
            "first_name": "New",
            "last_name": "Driver",
            "password": "newpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
