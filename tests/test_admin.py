from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number"
        )

    def test_driver_license_number_field(self):
        url = reverse("admin:taxi_driver_changelist") #?
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_admin_delail_license_number_field(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
# more tests?
