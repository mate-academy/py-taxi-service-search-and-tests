from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            first_name="admin2",
            last_name="miwa1",
            license_number="MVO28523"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="1qazcde3",
            first_name="Driver",
            last_name="Driver_name",
            license_number="MVO28593"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
