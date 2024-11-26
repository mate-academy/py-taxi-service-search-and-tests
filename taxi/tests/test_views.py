from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="u1s2e3r4"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Helicopter")

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="u1s2e3r4"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "hoakin",
            "password1": "a0s9d8f7",
            "password2": "a0s9d8f7",
            "first_name": "Hoa",
            "last_name": "Kin",
            "license_number": "PLO19283"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
