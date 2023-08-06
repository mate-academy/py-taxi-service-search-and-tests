from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin11",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="test first",
            last_name="test last",
            password="test1234",
            license_number="ABC12346"
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set = [self.driver.pk]

    def test_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_license_number_is_in_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")

    def test_license_number_is_in_fieldsets(self):
        url = "http://127.0.0.1:8000/admin/taxi/driver/1/change/"
        response = self.client.get(url)

        self.assertContains(response, "license_number")
