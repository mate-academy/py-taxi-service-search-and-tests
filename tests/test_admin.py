from django.test import TestCase

from django.test import Client
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class AdminTestCase(TestCase):
    def setUp(self):
        self.admin = Driver.objects.create_superuser("test_admin",
                                                     "EMAIL",
                                                     "0000")
        self.client = Client()
        self.client.force_login(self.admin)
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver = Driver.objects.create_user(
            username="test",
            password="PASSWORD",
            license_number="ASD1221"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_car_list_has_filter(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "manufacturer")

    def test_car_list_has_searching(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "model")

    def test_driver_list_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_change_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_assign_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.car.drivers.filter(
                pk=self.driver.pk).exists()
        )
