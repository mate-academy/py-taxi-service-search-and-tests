from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admintest",
            password="1qazcde3",
            license_number="ABC12345"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="authortest",
            password="2wsxvfr4",
            license_number="ABC12365"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test-country",
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )

    def test_driver_license_number_listed_in_changelist(self):
        """
        DriverAdmin: license_number appears in list_display.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_listed_in_detail_page(self):
        """
        DriverAdmin: license_number visible in change form.
        """
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_admin_add_page_contains_license_number(self):
        """
        DriverAdmin: add_fieldsets include license_number.
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")

    def test_car_admin_filter_exists(self):
        """
        CarAdmin: list_filter shows manufacturer filter on changelist.
        """
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, "manufacturer")

    def test_car_admin_search_works(self):
        """
        CarAdmin: search_fields includes 'model'.
        """
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "test"})
        self.assertContains(res, "test")
