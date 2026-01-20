from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

from taxi.admin import CarAdmin
from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_create_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_car_search_field_exists(self):
        url = reverse("admin:taxi_car_changelist") + "?q=Corolla"
        res = self.client.get(url)

        self.assertContains(res, self.car.model)

    def test_car_list_filter_displayed(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, "manufacturer")
