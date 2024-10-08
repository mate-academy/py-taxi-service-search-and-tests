from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class AdminTestCase(TestCase):
    """Tests for Django admin customization."""
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="test123456",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country",
        )

        self.car = Car.objects.create(
            model="test car",
            manufacturer=self.manufacturer,
        )

    def test_license_number_listed(self):
        """Test that driver's license number
        is in list display on admin page."""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_car_model_search(self):
        """Test that car can be searched by model in admin."""
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.car.model)

    def test_manufacturer_displayed(self):
        """Test that manufacturer is displayed correctly in admin."""
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.manufacturer.name)
