from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin.56789"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="John", password="john123456", license_number="ADC54768"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        request = self.client.get(url)

        self.assertContains(request, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        request = self.client.get(url)

        self.assertContains(request, self.driver.license_number)
