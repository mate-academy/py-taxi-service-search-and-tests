from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

BASE_URL = reverse("taxi:index")


class PublicTest(TestCase):
    def test_login_required(self):
        testing_url = self.client.get(BASE_URL)
        self.assertNotEqual(testing_url.status_code, 200)
        self.assertNotEqual(self.client.get(
            reverse("taxi:car-list")).status_code, 200
        )
        self.assertNotEqual(self.client.get(
            reverse("taxi:manufacturer-list")).status_code, 200
        )
        self.assertNotEqual(self.client.get(
            reverse("taxi:manufacturer-create")).status_code, 200
        )
        self.assertNotEqual(self.client.get(
            reverse("taxi:driver-list")).status_code, 200
        )


class PrivateDriverViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Ukraine"
        )
        self.car1 = Car.objects.create(
            model="310",
            manufacturer=self.manufacturer1
        )
        self.car1.drivers.add(self.user)

        self.client.force_login(self.user)

    def test_permission_accept(self):
        testing_url = self.client.get(BASE_URL)
        self.assertEqual(testing_url.status_code, 200)
        self.assertEqual(self.client.get(
            reverse("taxi:car-list")).status_code, 200
        )
        self.assertEqual(self.client.get(
            reverse("taxi:manufacturer-list")).status_code, 200
        )
        self.assertEqual(self.client.get(
            reverse("taxi:manufacturer-create")).status_code, 200
        )
        self.assertEqual(self.client.get(
            reverse("taxi:driver-list")).status_code, 200
        )

    def test_toggle_assign_to_car(self):
        self.car1.drivers.remove(self.user)
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car1.pk])
        )
        self.assertIn(self.user, self.car1.drivers.all())
        self.assertRedirects(response, reverse(
            "taxi:car-detail", args=[self.car1.pk])
        )

    def test_toggle_remove_from_car(self):
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car1.pk])
        )
        self.assertNotIn(self.user, self.car1.drivers.all())
        self.assertRedirects(response, reverse(
            "taxi:car-detail", args=[self.car1.pk])
        )
