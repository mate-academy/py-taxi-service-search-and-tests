from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "UNI67890"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)


class PrivateToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User",
            license_number="LICENSE123"
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

    def test_assign_driver_to_car(self):
        self.assertNotIn(self.car, self.user.cars.all())
        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id]
            )
        )
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.car.id]
            )
        )
