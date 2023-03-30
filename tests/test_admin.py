from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user2",
            password="admin123",
            first_name="Admin2",
            last_name="User2",
            license_number="ABC12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_superuser(
            username="driver",
            password="driver123",
            first_name="Test111",
            last_name="Test111",
            license_number="TST12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country",
        )
        self.car1 = Car.objects.create(
            model="Model 1",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Model 2",
            manufacturer=self.manufacturer
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        data = {
            "username": "newdriver",
            "password1": "newpass123",
            "password2": "newpass123",
            "first_name": "New",
            "last_name": "Driver",
            "license_number": "NEW45678",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(
            username="newdriver"
        ).exists())

        new_driver = get_user_model().objects.get(username="newdriver")
        self.assertEqual(new_driver.first_name, "New")
        self.assertEqual(new_driver.last_name, "Driver")
        self.assertEqual(new_driver.license_number, "NEW45678")

    def test_car_search(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url, {"q": "Model 1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")
        self.assertNotContains(response, "Model 2")

    def test_car_filter_by_manufacturer(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(
            url,
            {"manufacturer__id__exact": self.manufacturer.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")
        self.assertContains(response, "Model 2")
