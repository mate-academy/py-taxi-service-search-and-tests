from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWsORD>",
        )

    def test_retrieve_manufacturers(self):

        Manufacturer.objects.create(name="poetry")
        Manufacturer.objects.create(name="drama")
        self.client.force_login(self.user)
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="<NAME>",
            password="<PASSWORD>",
            first_name="test",
            last_name="test",
            license_number="YYY88877",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "<NAME>",
            "password1": "<PASSWORD>",
            "password2": "<PASSWORD>",
            "first_name": "test",
            "last_name": "test",
            "license_number": "YYY88877",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
