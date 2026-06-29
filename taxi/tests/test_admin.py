from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.admin_user = (
            get_user_model().objects.create_superuser(
                username="admin",
                password="admin12345",
                license_number="ADM12345",
            )
        )

        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password",
            license_number="AX1234BB",
        )

    def test_driver_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")

        response = self.client.get(url)

        self.assertContains(
            response,
            self.driver.license_number,
        )

    def test_driver_detail_license_number_listed(self) -> None:
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.pk],
        )

        response = self.client.get(url)

        self.assertContains(
            response,
            self.driver.license_number,
        )

    def test_driver_create_page_contains_required_fields(self) -> None:
        url = reverse("admin:taxi_driver_add")

        response = self.client.get(url)

        form = response.context["adminform"].form

        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("license_number", form.fields)
