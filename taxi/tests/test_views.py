from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
Driver = get_user_model()


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
        self.user = Driver.objects.create_user(
            username="new_driver",
            license_number="ADM12346",
            password="1qazcde3",
            first_name="Name",
            last_name="Surname",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_driver1",
            "license_number": "ADM12336",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Driver",
            "last_name": "Test",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_driver = Driver.objects.get(username=form_data["username"])
        self.assertEqual(new_driver.username, form_data["username"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
        self.assertTrue(new_driver.check_password(form_data["password1"]))
