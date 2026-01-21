from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriverpassword",
            license_number="BBB12345"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response_test = self.client.get(url)
        self.assertContains(response_test, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response_test = self.client.get(url)
        self.assertContains(response_test, self.driver.license_number)

    def test_driver_license_in_add_form(self):
        url = reverse("admin:taxi_driver_add")
        response_test = self.client.get(url)
        self.assertContains(response_test, "license_number")
