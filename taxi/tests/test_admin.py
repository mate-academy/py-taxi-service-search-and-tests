from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="PASSWORD123",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            license_number="ABC12345",
        )

    def test_driver_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_fields(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
        self.assertContains(res, self.driver.license_number)
        self.assertContains(res, "Additional info")

    def test_car_search_fields(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )

        url = reverse("admin:taxi_car_changelist") + "?q=Test"
        res = self.client.get(url)

        self.assertContains(res, car.model)

    def test_car_list_filter(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer 1", country="Country 1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer 2", country="Country 2"
        )
        car1 = Car.objects.create(
            model="Car 1",
            manufacturer=manufacturer1,
        )
        car2 = Car.objects.create(
            model="Car 2",
            manufacturer=manufacturer2,
        )

        url = (
            reverse("admin:taxi_car_changelist") + f"?manufacturer__id= "
            f"{manufacturer1.id}"
        )
        res = self.client.get(url)
        self.assertContains(res, car1.model)
        self.assertNotContains(res, car2.model)

    def test_manufacturer_listed(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, manufacturer.name)
        self.assertContains(res, manufacturer.country)
