from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from taxi.admin import DriverAdmin, CarAdmin
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth.hashers import make_password
from django.contrib import admin


class DriverAdminTest(TestCase):
    def setUp(self):
        password = make_password("password")
        self.driver = Driver.objects.create(
            username="testuser",
            password=password,
            first_name="John",
            last_name="Doe",
            license_number="JDO12345",
        )
        self.site = AdminSite()
        self.request = RequestFactory().get("/admin")
        self.ma = DriverAdmin(Driver, self.site)

    def test_license_number_in_list_display(self):
        self.assertIn("license_number", self.ma.list_display)

    def test_license_number_in_fieldsets(self):
        fieldsets = dict(self.ma.get_fieldsets(self.request))
        self.assertIn("license_number", fieldsets["Additional info"]["fields"])


class CarAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=manufacturer
        )
        self.ma = CarAdmin(Car, self.site)

    def test_search_fields(self):
        self.assertEqual(self.ma.search_fields, ("model",))

    def test_list_filter(self):
        self.assertEqual(self.ma.list_filter, ("manufacturer",))


class ManufacturerAdminTest(TestCase):
    def test_manufacturer_registered(self):
        self.assertTrue(Manufacturer in admin.site._registry)
