from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country"
        )

    def test_manufacturer_create_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete", args=[self.manufacturer.id]
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country"
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_create_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]
        ))
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete", args=[self.manufacturer.id]
        ))
        self.assertEqual(res.status_code, 200)

    def test_search_by_name_in_manufacturer_list(self):
        for num in range(3):
            Manufacturer.objects.create(
                name=f"manufacturer{num}",
                country=f"country{num}"
            )
        search_word = "manufacturer2"
        response = self.client.get(f"{MANUFACTURERS_URL}?field={search_word}")
        searched_query = Manufacturer.objects.filter(
            name__icontains=search_word
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], searched_query
        )


