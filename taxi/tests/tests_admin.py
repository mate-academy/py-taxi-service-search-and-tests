from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine",
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer2
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_car_search_by_model(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url, {"q": "Test"})

        self.assertContains(response, self.car.model)
