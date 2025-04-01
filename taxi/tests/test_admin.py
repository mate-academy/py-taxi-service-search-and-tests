from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from taxi.admin import CarAdmin, DriverAdmin
from taxi.models import Car, Manufacturer, Driver


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="Test License"
        )

    def test_driver_license_number_listed(self):
        """
        Test that license_number is in list_display on Driver admin page
        :return:
        """
        res = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(res, self.driver.license_number)

    def test_driver_group_name_listed(self):
        """
         Test that 'Groups' column if driver shown
        :return:
        """
        res = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(res, "Groups")

    def test_driver_detail_license_number_listed(self):
        """
        Test that license_number is in fields on Driver detail admin page
        :return:
        """
        res = self.client.get(
            reverse(
                "admin:taxi_driver_change",
                args=[self.driver.pk]
            )
        )
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fields_listed(self):
        """
        Test that first_name, last_name,license_number is in list_display
        on Driver detail admin page
        :return:
        """
        res = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertContains(res, "First name:")
        self.assertContains(res, "Last name:")
        self.assertContains(res, "License number:")

    def test_car_drivers_listed(self):
        """
        Test that drivers is in cars list page
        :return:
        """
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(model="TestCar", manufacturer=manufacturer)
        car.drivers.set([self.driver])
        res = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertContains(res, self.driver.username)

    def test_show_groups_output(self):
        """
        Test that show_groups method returns comma-separated group names
        """
        group = Group.objects.create(name="test_group")
        self.driver.groups.set([group])

        driver_admin_instance = DriverAdmin(Driver, admin.site)
        result = driver_admin_instance.show_groups(self.driver)

        self.assertEqual(result, group.name)

    def test_display_drivers_output(self):
        """
        Test that display_drivers method works correctly
        :return:
        """
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(model="TestCar", manufacturer=manufacturer)
        car.drivers.set([self.driver])

        car_admin_instance = CarAdmin(Car, admin.site)
        result = car_admin_instance.display_drivers(car)

        self.assertEqual(result, self.driver.username)
