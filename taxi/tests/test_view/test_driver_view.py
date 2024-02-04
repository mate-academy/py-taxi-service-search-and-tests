from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):
    def test_list_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_get_content_data(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertIsInstance(
            res.context["search_form"],
            DriverSearchForm
        )

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "AAA12345",
        }
        self.client.post(DRIVER_CREATE_URL, form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.first_name, form_data["first_name"])
        self.assertEqual(user.last_name, form_data["last_name"])
        self.assertEqual(user.license_number, form_data["license_number"])
