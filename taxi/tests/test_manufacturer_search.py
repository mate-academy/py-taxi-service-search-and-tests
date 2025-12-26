from django.contrib.auth import get_user_model

from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")


class PrivateManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )

        self.client.force_login(self.user)

    def test_manufacturers_search(self):
        Manufacturer.objects.create(
            name="First test",
            country="test"
        )
        Manufacturer.objects.create(
            name="SECOND TEST",
            country="test"
        )
        Manufacturer.objects.create(name="Last", country="test")

        searching_data = {"name": "test"}
        resp = self.client.get(MANUFACTURERS_LIST_URL, data=searching_data)
        manufacturers = Manufacturer.objects.filter(
            name__icontains="test"
        )
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers)
        )
