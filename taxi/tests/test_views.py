from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        resp = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(user=self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1")
        Manufacturer.objects.create(name="test2")

        resp = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response=resp, template_name="taxi/manufacturer_list.html"
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(user=self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345"
        }

        self.client.post(path=DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
