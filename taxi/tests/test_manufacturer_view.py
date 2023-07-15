from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

PK = "1"

MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE = reverse("taxi:manufacturer-update", args=[PK])
MANUFACTURER_DELETE = reverse("taxi:manufacturer-delete", args=[PK])


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        for _ in range(3):
            Manufacturer.objects.create(
                name=f"Test {_}",
                country="Test Kingdom"
            )

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST)

        self.assertNotEquals(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(MANUFACTURER_CREATE)

        self.assertNotEquals(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        response = self.client.get(MANUFACTURER_UPDATE)

        self.assertNotEquals(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        response = self.client.get(MANUFACTURER_DELETE)

        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )

        self.client.force_login(self.user)

        for _ in range(3):
            Manufacturer.objects.create(
                name=f"Test {_}",
                country="Test Kingdom"
            )

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST)

        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_by_name_manufacturer(self):
        Manufacturer.objects.create(
            name="New manufacturer",
            country="Test Kingdom"
        )

        response = self.client.get(MANUFACTURER_LIST + "?name=test")

        self.assertNotContains(response, "New manufacturer")
        self.assertContains(response, "name=\"name\" value=\"test\"")

    def test_search_by_name_pagination(self):
        for _ in range(15):
            Manufacturer.objects.create(
                name=f"New manufacturer {_}",
                country="Test Kingdom"
            )

        response = self.client.get(MANUFACTURER_LIST + "?name=new&page=2")

        self.assertNotContains(response, "Test 1")
        self.assertContains(response, "name=\"name\" value=\"new\"")
        self.assertContains(response, "New manufacturer 13")

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(MANUFACTURER_CREATE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_manufacturer_update(self):
        response = self.client.get(MANUFACTURER_UPDATE)

        self.assertEquals(response.status_code, 200)

    def test_retrieve_manufacturer_delete(self):
        response = self.client.get(MANUFACTURER_DELETE)

        self.assertEquals(response.status_code, 200)
