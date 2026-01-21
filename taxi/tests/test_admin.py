from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.driver = Driver.objects.create_user(
            username="driver",
            password="testdriver",
            license_number="ABC123456"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license number is in list_display
        on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_car_model_searchable(self):
        """
        Test that car model is searchable in the admin page
        """
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url + "?q=Camry")
        self.assertContains(res, self.car.model)

    def test_manufacturer_listed(self):
        """
        Test that manufacturer is listed in the admin page
        """
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.manufacturer.name)
