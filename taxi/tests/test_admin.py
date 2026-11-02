from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin123",
            license_number="ADM00001",
        )
        self.client.force_login(self.admin)

        self.driver = get_user_model().objects.create_user(
            username="driver", license_number="TST00001"
        )

    def test_license_number_in_driver_list(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_license_number_on_driver_change_page(self):
        response = self.client.get(
            reverse("admin:taxi_driver_change", args=[self.driver.pk])
        )
        self.assertContains(response, self.driver.license_number)

    def test_custom_fields_on_driver_add_page(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))

        for field in ("first_name", "last_name", "license_number"):
            with self.subTest(field=field):
                self.assertContains(response, f'name="{field}"')
