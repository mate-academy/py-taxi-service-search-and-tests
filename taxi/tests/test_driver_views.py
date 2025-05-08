from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
)

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverViewsTests(TestCase):
    def test_access_not_logged_in_users(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

    def test_driver_list_view(self):
        res = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]), list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], self.user)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_driver_create_view_get(self):
        url = reverse("taxi:driver-create")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], DriverCreationForm)
        self.assertTemplateUsed(res, "taxi/driver_form.html")

    def test_driver_create_view_post(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "new_test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "New",
            "last_name": "User",
            "license_number": "XYZ12345"
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            Driver.objects.filter(username="new_test_user").exists()
        )

    def test_driver_license_update_view_get(self):
        url = reverse("taxi:driver-update", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], DriverLicenseUpdateForm)
        self.assertTemplateUsed(res, "taxi/driver_form.html")

    def test_driver_license_update_view_post(self):
        url = reverse("taxi:driver-update", args=[self.user.id])
        data = {
            "license_number": "DEF67890"
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "DEF67890")

    def test_driver_delete_view_get(self):
        url = reverse("taxi:driver-delete", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "taxi/driver_confirm_delete.html"
        )

    def test_driver_delete_view_post(self):
        url = reverse("taxi:driver-delete", args=[self.user.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Driver.objects.filter(id=self.user.id).exists())

    def test_driver_search(self):
        url = f"{DRIVER_LIST_URL}?username=test"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 1)
        self.assertEqual(res.context["driver_list"][0], self.user)

    def test_toggle_assign_to_car(self):
        # Test assigning a car to the driver
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())

        # Test unassigning the car from the driver
        res = self.client.get(url)

        self.assertEqual(res.status_code, 302)
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
