from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.admin import DriverAdmin, CarAdmin
from taxi.models import Driver, Car, Manufacturer


class MockSuperUser:
    def has_perm(self, perm):
        return True


class AdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin"
        )
        self.site = AdminSite()

        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = self.user

        self.driver = Driver.objects.create(
            username="driver1",
            email="driver1@example.com",
            password="password1",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Toyota Corolla",
            manufacturer=Manufacturer.objects.create(
                name="Toyota",
                country="Japan"
            ),
        )

    def test_driver_admin_list_display(self):
        driver_admin = DriverAdmin(Driver, self.site)
        self.assertTrue("license_number" in driver_admin.list_display)

    def test_driver_admin_fieldsets(self):
        driver_admin = DriverAdmin(Driver, self.site)
        form = driver_admin.get_form(self.request, self.driver)
        form_instance = form(instance=self.driver)
        self.assertIn("license_number", form_instance.fields)

    def test_car_admin_search_fields(self):
        car_admin = CarAdmin(Car, self.site)
        self.assertTrue("model" in car_admin.search_fields)

    def test_car_admin_list_filter(self):
        car_admin = CarAdmin(Car, self.site)
        self.assertTrue("manufacturer" in car_admin.list_filter)

    def test_manufacturer_registered(self):
        self.client.login(
            username="admin",
            email="admin@admin.com",
            password="admin"
        )
        response = self.client.get("/admin/taxi/manufacturer/")
        self.assertEqual(response.status_code, 200)

    def test_admin_login_and_access_driver_page(self):
        self.client.login(username="admin", password="admin")
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
