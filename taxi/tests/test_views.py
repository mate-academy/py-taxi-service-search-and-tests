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
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test_manufacturer",
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
