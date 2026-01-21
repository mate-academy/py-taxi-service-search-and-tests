from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",

        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Tesla_t", country="USA")
        Manufacturer.objects.create(name="Tesla_tx", country="USA")
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers)
                         )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passtest2"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "usertest",
            "password1": "testpass12",
            "password2": "testpass12",
            "first_name": "nametest",
            "last_name": "lasttest",
            "license_number": "LWE12332"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
