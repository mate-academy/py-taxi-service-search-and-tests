from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="testdriver", license_number="ZXC19876"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="USA"
        )
        self.car = Car.objects.create(
            model="Test Model", manufacturer=self.manufacturer
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number is in list_display a driver admin
        page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is in a driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
