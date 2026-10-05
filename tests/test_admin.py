from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Driver


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@test",
            password="testadmin1"
        )
        self.client.force_login(self.admin_user)
        self.driver: Driver = Driver.objects.create_user(
            username="testdriver",
            first_name="testname",
            last_name="testlastname",
            license_number="ABC12345"
        )

    def test_drivers_additional_info_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
