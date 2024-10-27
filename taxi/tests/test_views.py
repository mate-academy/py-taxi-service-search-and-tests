from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase

from taxi.models import Driver, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(username="Test", license_number="123456")
        Driver.objects.create(username="Second", license_number="4453453")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        form_date = {
            "name": "test",
            "country": "test",
            "password1": "user14Test",
            "password2": "user14Test",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_date)
        new_manufacturer = Manufacturer.objects.get(name=form_date["name"])

        self.assertEqual(new_manufacturer.country, form_date["country"])
