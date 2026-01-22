from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test driver",
            license_number="QAZ12345"
        )
        for num in range(1, 3):
            self.manufacturer = Manufacturer.objects.create(
                name=f"test manufacturer{num}"
            )
        self.car1 = Car.objects.create(
            model="test car1",
            manufacturer_id=1,
        )
        self.car2 = Car.objects.create(
            model="test car2",
            manufacturer_id=2,
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_car_list_filter_by_manufacturer(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.car1.manufacturer)
