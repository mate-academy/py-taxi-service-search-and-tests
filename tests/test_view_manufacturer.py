from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer_count = 5

        for i in range(manufacturer_count):
            Manufacturer.objects.create(
                name=f"manufacturer{i}",
                country=f"country{i}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_list_search_by_name(self):
        search_value = "4"
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": search_value}
        )
        manufacturers = Manufacturer.objects.filter(
            name__icontains=search_value
        )

        self.assertQuerysetEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
