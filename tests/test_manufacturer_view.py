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
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEquals(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name",
            country="manufacturer_country"
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": "manufacturer_name"}
        )
        self.assertEquals(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]
        self.assertEquals(len(manufacturers), 1)
        self.assertEquals(manufacturers[0].name, "manufacturer_name")

    def test_manufacturer_search_with_no_result(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "unknown"})
        manufacturers = response.context["manufacturer_list"]
        self.assertEquals(len(manufacturers), 0)
