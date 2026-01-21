from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="Test", password="test-password"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="Test_driver",
            license_number="AAA11111",
            first_name="Some",
            last_name="Driver",
            password="driver-password",
        )

    def test_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_licence_number(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
