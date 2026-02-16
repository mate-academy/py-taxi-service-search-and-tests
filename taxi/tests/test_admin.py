from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="JOD26458",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country",
        )

        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_driver_license_number_listed(self):
        """Test list_display license_number field"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Test fieldsets license_number field"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_license_number_first_name_last_name_listed(self):
        """Test first_name, last_name, license_number in add_fieldsets"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        form_fields = response.context["adminform"].form.fields
        self.assertIn("first_name", form_fields)
        self.assertIn("last_name", form_fields)
        self.assertIn("license_number", form_fields)

    def test_car_search_display(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, 'name="q"')

    def test_car_search_by_model(self):
        url = reverse("admin:taxi_car_changelist")
        # making url with query parameters
        response = self.client.get(url, {"q": self.car.model})
        self.assertContains(response, self.car.model)

    def test_car_filter_by_manufacturer(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(
            url, {"manufacturer__id__exact": self.manufacturer.id}
        )
        self.assertContains(response, self.car.model)
