from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverFormatTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverFormatTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user123",
            password="test_pass1234456",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        username = "test_username"
        password = "password2145"
        license_number = "test_license_number"
        get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        response = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        response = self.client.get("/drivers/?username=username_test")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="username_test")
        )
