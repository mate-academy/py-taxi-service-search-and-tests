from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.admin import CarAdmin
from taxi.models import Driver, Manufacturer, Car


class AdminSiteTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.car_admin = CarAdmin(Car, AdminSite())
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123",
            email="admin@test.com"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_driver_admin_display_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")

    def test_car_list_filters(self):
        self.assertIn("manufacturer", self.car_admin.list_filter)
