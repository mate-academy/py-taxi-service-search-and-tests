from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriversTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriversTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="test1",
            password="test1234",
            first_name="testfirst",
            last_name="testlast",
            license_number="TET12345",
        )
        Driver.objects.create(
            username="test2",
            password="test12345",
            first_name="testfirst1",
            last_name="testlast1",
            license_number="TEA12345",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "newdriver2",
            "password1": "passw0rdTest",
            "password2": "passw0rdTest",
            "first_name": "testfirst",
            "last_name": "testlast",
            "license_number": "TEZ12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
