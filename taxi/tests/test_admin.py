from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="LOL12345",
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license number is in
         list _display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Test that driver's license number is in driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car1 = Car.objects.create(model="RAV4", manufacturer=manufacturer)
        car2 = Car.objects.create(model="Camry", manufacturer=manufacturer)
        search_url = reverse("admin:taxi_car_changelist") + "?q=RAV4"
        response = self.client.get(search_url)
        self.assertContains(response, car1.model)
        self.assertNotContains(response, car2.model)
