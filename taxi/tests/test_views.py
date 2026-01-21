from http.client import responses
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListViewTest(TestCase):
    def test_public_access_to_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            username="test_name",
            password="password_test12345"
        )
        self.client.force_login(user)

    def test_private_access_to_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed("taxi/manufacturer_list.html")
