from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.test import TestCase, Client
from django.urls import reverse

from taxi.admin import DriverAdmin
from taxi.models import Driver


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="<PASSWORD>",
            license_number="GGG11111",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_displayed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_inherits_useradmin_functionalities(self):
        driver_admin = DriverAdmin(Driver, admin.site)
        self.assertEqual(
            driver_admin.list_display,
            UserAdmin.list_display + ("license_number",)
        )
        self.assertEqual(
            driver_admin.fieldsets,
            UserAdmin.fieldsets
            + (("Additional info", {"fields": ("license_number",)}),),
        )
        self.assertEqual(
            driver_admin.add_fieldsets,
            UserAdmin.add_fieldsets
            + (
                (
                    (
                        "Additional info",
                        {
                            "fields": (
                                "first_name",
                                "last_name",
                                "license_number",
                            )
                        },
                    ),
                )
            ),
        )
