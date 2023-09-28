from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="LAM12345",
        )
        # self.manufacturer = Manufacturer.objects.create(
        #     name="BMW",
        #     country="Germany"
        # )
        # self.car = Car.objects.create(
        #     model="M3",
        #     manufacturer=self.manufacturer
        # )
        # self.car.drivers.add(self.driver)

    def test_driver_license_listed(self):
        """Test that license listed in drivers list page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        """Test that license listed in drivers detail page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_admin_add_fieldsets(self):
        """Test that 'License number' field listed"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "License number")
