from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


DRIVERS_URL = reverse("taxi:driver-list")
PAGINATION = 1


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Paul",
            license_number="KIA19754",
            first_name="Paul",
            last_name="Maslov",
            password="Platina07",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "KIA12235"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_car_list_response_with_correct_template(self):
        response = self.client.get(DRIVERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_list_paginated_correctly(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(len(response.context["driver_list"]), PAGINATION)

    def test_car_detail_response_with_correct_template(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_search_driver_form(self):
        response = self.client.get(DRIVERS_URL + "?username=John")

        self.assertContains(response, "John")
        self.assertNotContains(response, "Michael")
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverLicenseUpdateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Paul",
            license_number="KIA19754",
            first_name="Paul",
            last_name="Maslov",
            password="Platina07",
        )
        self.client.force_login(self.user)

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "KIA34526"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "BF82"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)
