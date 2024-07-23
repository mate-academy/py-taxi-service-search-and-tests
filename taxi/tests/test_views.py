from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        Manufacturer.objects.create(
            name="test1",
            country="country2"
        )
        responce = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(responce.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(responce.context["manufacturer_list"]),
            list(manufacturer)
        )
