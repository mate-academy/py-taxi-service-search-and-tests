from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin_username",
            password="Pass1234!",
            license_number="ADM11111"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123!",
            license_number="DVR12345"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(
            response,
            self.driver.license_number,
        )

    def test_driver_custom_add_fields(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="license_number"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="license_number"')

    def test_license_number_in_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=(self.driver.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="license_number"')

    def test_car_search_field(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'id="searchbar"')

    def test_car_list_filter(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer1
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer2
        )
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "By manufacturer")
