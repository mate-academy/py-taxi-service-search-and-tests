from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin

from taxi.models import Car, Manufacturer
from taxi.admin import DriverAdmin, CarAdmin


class DriverAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Elon",
            last_name="Musk",
            license_number="XYZ789",
        )

    def test_license_number(self):
        driver_admin_instance = DriverAdmin(get_user_model(), self.site)
        self.assertEqual(
            driver_admin_instance.list_display,
            UserAdmin.list_display + ('license_number',)
        )


class CarAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Elon",
            last_name="Musk",
            license_number="XYZ789",
        )
        self.car.drivers.add(self.driver)

    def test_search_fields(self):
        car_admin_instance = CarAdmin(Car, self.site)
        self.assertEqual(car_admin_instance.search_fields, ('model',))

    def test_list_filter(self):
        car_admin_instance = CarAdmin(Car, self.site)
        self.assertEqual(car_admin_instance.list_filter, ('manufacturer',))
