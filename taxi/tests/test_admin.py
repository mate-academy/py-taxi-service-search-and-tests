from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA00000",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license_number is on
        list_display on driver admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license_number is on driver detail admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_create_page_has_fields(self):
        """
        Test that the add driver admin page contains first_name,
        last_name, and license_number fields.
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="first_name"')
        self.assertContains(res, 'name="last_name"')
        self.assertContains(res, 'name="license_number"')


class CarAdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )

    def test_car_admin_search_box_exists(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="q"')
