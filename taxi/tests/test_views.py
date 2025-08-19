from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            license_number="ADM12346",
            first_name="Name",
            last_name="Surname",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Manufacturer", country="Country")
        Manufacturer.objects.create(name="Manufacturer2", country="Country2")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            license_number="ADM12346",
            password="1qazcde3",
            first_name="Name",
            last_name="Surname",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "admin",
            "license_number": "ADM12346",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Name",
            "last_name": "Surname",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertTrue(new_user.check_password(form_data["password1"]))
