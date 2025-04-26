from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_driver_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username_test",
            password="test_password",
            license_number="ABC00000",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="test.user",
            password="test_password",
            license_number="ABC11111",
        )
        Driver.objects.create(
            username="driver_name",
            password="test_password",
            license_number="ABC22222",
        )
        Driver.objects.create(
            username="names",
            password="test_password",
            license_number="ABC33333",
        )

    def test_create_driver(self):
        form_data = {
            "username": "username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC44444",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )

    def test_driver_retrieve_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_form_in_manufacturer(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "user"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "test.user")
        self.assertContains(response, "username_test")
        self.assertNotContains(response, "driver_name")
        self.assertNotContains(response, "names")
