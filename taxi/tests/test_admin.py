from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = self.client_class()
        self.admin_user = Driver.objects.create_superuser(
            username="adminuser",
            password="password123",
            license_number="ABC123456",
            first_name="Narberal",
            last_name="Gamma",
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            license_number="DEF987654",
            first_name="John",
            last_name="Doe",
        )
        self.car = Car.objects.create(
            model="Supra",
            manufacturer=self.manufacturer
        )

    def test_driver_admin_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_admin_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")

    def test_car_admin_search(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "Supra"})
        self.assertContains(res, self.car.model)
