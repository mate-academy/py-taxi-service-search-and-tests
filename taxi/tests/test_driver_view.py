from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):

    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create_user(
            username="testdriver1",
            password="password123",
            first_name="Test1",
            last_name="Driver1",
            license_number="ABC1231"
        )
        Driver.objects.create_user(
            username="testdriver2",
            password="password123",
            first_name="Test2",
            last_name="Driver2",
            license_number="ABC1232"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_driver",
            "password1": "new_password123",
            "password2": "new_password123",
            "first_name": "Test3",
            "last_name": "Driver3",
            "license_number": "GHI45789"
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(
            new_driver.first_name, form_data["first_name"])
        self.assertEqual(
            new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"])
