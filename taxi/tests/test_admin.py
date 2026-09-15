from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.admin import CarAdmin, DriverAdmin
from taxi.models import Car, Driver


class AdminTests(TestCase):
    def test_driver_admin_registered(self):
        self.assertIn(Driver, site._registry)
        self.assertIsInstance(site._registry[Driver], DriverAdmin)

    def test_driver_admin_list_display(self):
        driver_admin = site._registry[Driver]
        self.assertIn("license_number", driver_admin.list_display)

    def test_driver_admin_fieldsets(self):
        driver_admin = site._registry[Driver]
        fieldsets = driver_admin.fieldsets
        fields = [
            field
            for section, options in fieldsets
            for field in options.get("fields", ())
        ]
        self.assertIn("license_number", fields)

    def test_driver_admin_add_fieldsets(self):
        driver_admin = site._registry[Driver]
        add_fieldsets = driver_admin.add_fieldsets
        fields = [
            field
            for section, options in add_fieldsets
            for field in options.get("fields", ())
        ]
        self.assertIn("license_number", fields)
        self.assertIn("first_name", fields)
        self.assertIn("last_name", fields)

    def test_car_admin_registered(self):
        self.assertIn(Car, site._registry)
        self.assertIsInstance(site._registry[Car], CarAdmin)

    def test_car_admin_search_fields_and_list_filter(self):
        car_admin = site._registry[Car]
        self.assertIn("model", car_admin.search_fields)
        self.assertIn("manufacturer", car_admin.list_filter)
