from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminCarTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@mail.com",
            password="123qwe",
        )
        self.client.force_login(user=self.admin)
        self.manufacturer1 = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="XXXX", country="TestCountry"
        )
        self.first_car = Car.objects.create(
            model="TestModel", manufacturer=self.manufacturer1
        )
        self.second_car = Car.objects.create(
            model="XXXX", manufacturer=self.manufacturer2
        )

    def test_car_in_admin_page(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"), {"q": "XX"}
        )
        self.assertContains(response, self.second_car.model)
        self.assertNotContains(response, self.first_car.model)

    def test_car_filter_by_manufacturer(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            {"manufacturer__id__exact": self.manufacturer2.id},
        )
        self.assertContains(response, self.second_car.model)
        self.assertNotContains(response, self.first_car.model)


class AdminDriverTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@mail.com",
            password="123qwe",
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        self.client.force_login(user=self.admin)

    def test_driver_in_admin_page(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_license_number_in_driver_changelist(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.user.license_number)

    def test_add_driver_license_number_in_additional_fields(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertContains(response, "Additional info")


class AdminManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@mail.com",
            password="123qwe",
        )
        self.client.force_login(user=self.admin)

    def test_manufacturer_in_admin_page(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
