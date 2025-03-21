from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            license_number="XYZ12345",
        )

    def test_admin_driver_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.username)
        self.assertContains(res, self.driver.license_number)

    def test_admin_driver_change_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_admin_driver_add_page(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_admin_manufacturer_listed(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertContains(res, manufacturer.name)
        self.assertContains(res, manufacturer.country)

    def test_admin_car_listed(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer)
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, car.model)
