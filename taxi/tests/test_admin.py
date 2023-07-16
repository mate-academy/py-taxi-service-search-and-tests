from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@test.com", password="password123"
        )
        self.client.force_login(self.admin_user)
        self.driver = Driver.objects.create(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            email="testdriver@test.com",
            license_number="ABC123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer", country="Test_Country"
        )
        self.car = Car.objects.create(
            model="Test_Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_driver_listed(self):
        """Test that drivers are listed on driver page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.username)
        self.assertContains(res, self.driver.license_number)

    def test_car_listed(self):
        """Test that cars are listed on car page"""
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.car.model)
        self.assertEqual(res.status_code, 200)

    def test_driver_page(self):
        """Test that license number present on the driver page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_page(self):
        """Test that license number present on the driver page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
