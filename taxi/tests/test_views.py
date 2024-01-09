from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.forms import DriverCreationForm

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="test123")
        Manufacturer.objects.create(name="test2", country="test321")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "",
            "last_name": "",
            "license_number": ""
        }
        response = self.client.post(reverse("taxi:driver-create"),
                                    data=form_data
                                    )
        form = response.context["form"]
        if not form.is_valid():
            print(form.errors)
        self.assertEqual(response.status_code, 200)

        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertIsNotNone(new_user)
        print(new_user)

        self.assertEqual(new_user.first_name, form_data["first_name"])
        print(new_user.first_name)
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
