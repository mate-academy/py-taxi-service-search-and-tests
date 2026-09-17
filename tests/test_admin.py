from django.test import TestCase
from django.contrib.admin.sites import site
from taxi.admin import DriverAdmin, CarAdmin
from taxi.models import Driver, Car


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.driver_admin = DriverAdmin(model=Driver, admin_site=site)
        self.car_admin = CarAdmin(model=Car, admin_site=site)

    def test_check_license_number_in_driver_admin_list_display(self):
        self.assertIn("license_number", self.driver_admin.list_display)

    def test_check_license_number_in_driver_admin_fieldsets(self):
        self.assertIn(
            ("Additional info", {"fields": ("license_number",)}),
            self.driver_admin.fieldsets,
        )

    def test_check_additional_info_in_driver_admin_add_fieldsets(self):
        cases = ["first_name", "last_name", "license_number"]

        for field in cases:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    str(self.driver_admin.add_fieldsets),
                )

    def test_check_model_in_car_admin_search_fields(self):
        self.assertIn(
            "model",
            self.car_admin.search_fields,
            msg="(model is not found in search_fields)",
        )

    def test_check_manufacturer_in_car_admin_list_filter(self):
        self.assertIn(
            "manufacturer",
            self.car_admin.list_filter,
            msg="(manufacturer is not found in list_filter)",
        )
