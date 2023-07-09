from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEquals(res.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Suzuki", country="Japan")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
