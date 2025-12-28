from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from taxi.admin import DriverAdmin, CarAdmin
from taxi.models import Driver, Manufacturer, Car


class DriverAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = DriverAdmin(Driver, self.site)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="password", license_number="AO8888AO"
        )

    def test_list_display(self):
        self.assertIn("license_number", self.admin.list_display)

    def test_addition_of_the_fieldsets(self):
        add_fieldsets = dict(
            (fs[0], [field for field in fs[1]["fields"]])
            for fs in self.admin.add_fieldsets
        )
        self.assertIn(
            "license_number",
            add_fieldsets.get("Additional info", [])
        )


class CarAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CarAdmin(Car, self.site)
        self.manufacturer = Manufacturer.objects.create(name="BMW")
        self.car = Car.objects.create(
            model="i4 Competition", manufacturer=self.manufacturer
        )

    def test_fields(self):
        self.assertIn("model", self.admin.search_fields)

    def test_filter(self):
        self.assertIn("manufacturer", self.admin.list_filter)
