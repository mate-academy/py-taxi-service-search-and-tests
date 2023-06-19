from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_list(self) -> None:
        result = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list(self) -> None:
        Manufacturer.objects.create(
            name="test1",
            country="country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="country2"
        )

        result = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEquals(result.status_code, 200)
        self.assertEquals(
            list(result.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )
