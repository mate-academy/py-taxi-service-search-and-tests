from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="13admin31"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="dirvertest",
            first_name="First",
            last_name="Lasts",
            license_number="CAD25252",
            password="drivepass22",
        )

    def test_driver_list_license_present(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_details_license_present(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_create_custom_fields_present(self) -> None:
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
