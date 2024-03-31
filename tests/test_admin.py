from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.admin import CarAdmin
from taxi.models import Car


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="12112008Qaz"
        )

        self.site = AdminSite()

        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="ABC12345"
        )

        self.car_admin = CarAdmin(Car, self.site)

    def test_driver_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_create_additional_info_listed(self) -> None:
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "id_license_number")
        self.assertContains(res, "id_first_name")
        self.assertContains(res, "id_last_name")

    def test_search_by_car_model(self) -> None:
        self.assertIn("model", self.car_admin.search_fields)

    def test_filtering_by_car_manufacturer(self) -> None:
        self.assertIn("manufacturer", self.car_admin.list_filter)
