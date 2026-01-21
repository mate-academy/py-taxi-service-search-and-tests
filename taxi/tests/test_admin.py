from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123user"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test123user",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self) -> None:
        """
        Test that driver's licence_number is in list_display
        on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        """
        Test that driver's license_number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_create_license_number_listed(self) -> None:
        """
        Test that license_number field is on driver create admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, 'name="license_number"')


class CarAdminTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123user"
        )
        self.client.force_login(self.admin_user)
        self.manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer
        )

    def test_car_model_should_be_in_search_field(self) -> None:
        """
        Test that car's model is in search_field on car's list page
        """
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "model")

    def test_car_manufacturer_should_be_in_list_filter(self) -> None:
        """
        Test that car's manufacturer is in list_filter on car's list page
        """
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "manufacturer")
